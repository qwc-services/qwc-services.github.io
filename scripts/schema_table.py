#!/usr/bin/env python3
"""Render a JSON schema as markdown tables.

The root schema is rendered as a table of its properties, nested properties
being indented below their parent. Each other schema file referenced through
$ref gets its own section with its own table, linked from the parent row.
"""

import json
import os
import re
import sys

USAGE = "Usage: schema_table.py <schema.json> <output.md>"
INDENT = "\u00a0" * 4


def escape(text):
    """Escape markdown outside code spans: placeholders like <path> would be parsed as HTML, | would split the table cell."""
    chunks = re.split(r"(`[^`]*`)", text.replace("\n", " "))
    return "".join(
        chunk if chunk.startswith("`") else chunk.replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")
        for chunk in chunks
    )


def is_array(node):
    return node.get("type") == "array" and isinstance(node.get("items"), dict)


def is_map(node):
    return node.get("type") == "object" and isinstance(node.get("additionalProperties"), dict)


class Renderer:
    def __init__(self, root_path):
        self.base_dir = os.path.dirname(os.path.abspath(root_path))
        self.schemas = {}
        # Schema files to render as own section, in discovery order
        self.sections = [os.path.basename(root_path)]

    def load(self, filename):
        if filename not in self.schemas:
            with open(os.path.join(self.base_dir, filename)) as fh:
                self.schemas[filename] = json.load(fh)
        return self.schemas[filename]

    def split_ref(self, ref, current_file):
        """Split a $ref relative to `current_file` into (file, JSON pointer)."""
        filename, _, pointer = ref.partition("#")
        return filename or current_file, pointer

    def resolve(self, ref, current_file):
        """Resolve a $ref relative to `current_file`, returning (file, node)."""
        filename, pointer = self.split_ref(ref, current_file)
        node = self.load(filename)
        for part in filter(None, pointer.split("/")):
            node = node[part]
        return filename, node

    def is_section_ref(self, ref, current_file):
        """Whether a $ref points to the root of another file, rendered as own section."""
        filename, pointer = self.split_ref(ref, current_file)
        return filename != current_file and not pointer

    def inline_ref(self, node, current_file):
        """Return the (file, pointer) of the $ref of node inlined in the current table, if any."""
        ref = node.get("$ref")
        if ref is None or self.is_section_ref(ref, current_file):
            return None
        return self.split_ref(ref, current_file)

    def anchor(self, filename):
        return "schema-" + os.path.splitext(filename)[0].lower()

    def section_link(self, filename):
        if filename not in self.sections:
            self.sections.append(filename)
        title = self.load(filename).get("title", filename)
        return f"[{title}](#{self.anchor(filename)})"

    def flatten(self, node, current_file):
        """Flatten inlined $ref and allOf into a single node, returning (node, file).

        A $ref to the root of another file is kept as is, since it is rendered as a link.
        """
        node = dict(node)
        ref = node.pop("$ref", None)
        if ref is not None:
            if self.is_section_ref(ref, current_file):
                node["$ref"] = ref
                return node, current_file
            current_file, target = self.resolve(ref, current_file)
            target, _ = self.flatten(target, current_file)
            node = {**target, **node}
        for sub in node.pop("allOf", []):
            sub, _ = self.flatten(sub, current_file)
            props = {**sub.get("properties", {}), **node.get("properties", {})}
            required = sub.get("required", []) + node.get("required", [])
            node = {**sub, **node}
            if props:
                node["properties"] = props
            if required:
                node["required"] = required
        return node, current_file

    def type_label(self, node, current_file):
        if "$ref" in node:
            return self.section_link(self.resolve(node["$ref"], current_file)[0])
        if "const" in node:
            return f"`{json.dumps(node['const'])}`"
        if "oneOf" in node:
            return "one of"
        types = node.get("type")
        if isinstance(types, list):
            return " \\| ".join(types)
        if is_array(node):
            items, items_file = self.flatten(node["items"], current_file)
            label = "array of " + self.type_label(items, items_file)
            size = node.get("minItems")
            if size is not None and size == node.get("maxItems"):
                label += f" [{size}]"
            return label
        if is_map(node):
            return "map"
        return types or ""

    def description(self, node, current_file, required, repeats):
        text = node.get("description")
        if not text and "$ref" in node:
            text = self.resolve(node["$ref"], current_file)[1].get("description")
        parts = [text] if text else []
        if "enum" in node:
            parts.append("One of " + ", ".join(f"`{v}`" for v in node["enum"]) + ".")
        if "default" in node:
            parts.append(f"Default: `{json.dumps(node['default'])}`.")
        if repeats:
            parts.append(f"Same structure as `{repeats}`, recursively.")
        if required:
            parts.append("**Required.**")
        return escape(" ".join(parts))

    def repeats(self, node, current_file, expanding_refs):
        """Return the field whose definition node expands again, if node is recursive."""
        flat, flat_file = self.flatten(node, current_file)
        candidates = [(node, current_file)]
        if is_array(flat):
            candidates.append((flat["items"], flat_file))
        for candidate, candidate_file in candidates:
            ref = self.inline_ref(candidate, candidate_file)
            if ref in expanding_refs:
                return expanding_refs[ref]
        return None

    def row(self, depth, field, node, current_file, expanding_refs, required=False):
        flat, flat_file = self.flatten(node, current_file)
        repeats = self.repeats(node, current_file, expanding_refs)
        return depth, field, self.type_label(flat, flat_file), self.description(flat, flat_file, required, repeats)

    def rows(self, node, current_file, depth, expanding_refs, field):
        """Yield (depth, field, type, description) rows for the children of the raw node.

        `expanding_refs` maps the inlined $refs being expanded to the field expanding them,
        to stop on recursive definitions.
        """
        ref = self.inline_ref(node, current_file)
        if ref in expanding_refs:
            return
        if ref is not None:
            expanding_refs = {**expanding_refs, ref: field}
        node, current_file = self.flatten(node, current_file)
        if "$ref" in node:
            return
        if is_array(node):
            yield from self.rows(node["items"], current_file, depth, expanding_refs, field)
            return
        if "oneOf" in node:
            for variant in node["oneOf"]:
                title = self.flatten(variant, current_file)[0].get("title", "variant")
                # Non-breaking spaces, so a wrapped title does not lose its indentation
                title = title.replace(" ", "\u00a0")
                yield self.row(depth, f"*{title}*", variant, current_file, expanding_refs)
                yield from self.rows(variant, current_file, depth + 1, expanding_refs, field)
            return
        required = set(node.get("required", []))
        for name, prop in node.get("properties", {}).items():
            yield self.row(depth, f"`{name}`", prop, current_file, expanding_refs, name in required)
            yield from self.rows(prop, current_file, depth + 1, expanding_refs, name)
        if is_map(node):
            additional = node["additionalProperties"]
            yield self.row(depth, "`<key>`", additional, current_file, expanding_refs)
            yield from self.rows(additional, current_file, depth + 1, expanding_refs, field)

    def table(self, filename):
        lines = ["| Field | Type | Description |", "|---|---|---|"]
        for depth, field, type_, desc in self.rows(self.load(filename), filename, 0, {}, None):
            lines.append(f"| {INDENT * depth}{field} | {type_} | {desc} |")
        return lines

    def render(self):
        out = self.table(self.sections[0])
        i = 1
        # Rendering a table may discover further sections, hence no plain for loop
        while i < len(self.sections):
            filename = self.sections[i]
            i += 1
            schema = self.load(filename)
            title = schema.get("title", filename)
            out += ["", f'#### {title} <a name="{self.anchor(filename)}"></a>', ""]
            if schema.get("description"):
                out += [escape(schema["description"]), ""]
            out += self.table(filename)
        return "\n".join(out) + "\n"


def main():
    if len(sys.argv) != 3:
        sys.exit(USAGE)
    output = Renderer(sys.argv[1]).render()
    with open(sys.argv[2], "w") as fh:
        fh.write(output)


if __name__ == "__main__":
    main()
