#!/usr/bin/env python3
"""Render a JSON schema as markdown tables.

The root schema is rendered as a table of its properties, nested properties
being indented below their parent. Each other schema file referenced through
$ref gets its own section with its own table, linked from the parent row.
"""

import itertools
import json
import os
import re
import sys

NBSP = "\u00a0"


def escape(text):
    """Escape markdown outside code spans: placeholders like <path> would be parsed as HTML, | would split the table cell."""
    chunks = re.split(r"(`[^`]*`)", text.replace("\n", " "))
    return "".join(
        chunk if chunk.startswith("`") else chunk.replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")
        for chunk in chunks
    )


def code(value):
    return f"`{json.dumps(value)}`"


def is_array(node):
    return node.get("type") == "array" and isinstance(node.get("items"), dict)


def is_map(node):
    return node.get("type") == "object" and isinstance(node.get("additionalProperties"), dict)


def anchor(filename):
    anchor_prefix = "schema-"
    return anchor_prefix + os.path.splitext(filename)[0].lower()


def split_ref(ref, current_file):
    """Split a $ref relative to `current_file` into (file, JSON pointer)."""
    filename, _, pointer = ref.partition("#")
    return filename or current_file, pointer


class Renderer:
    def __init__(self, root_path):
        self.base_dir = os.path.dirname(os.path.abspath(root_path))
        self.schemas = {}
        # Root schema file first, then the referenced files rendered as own section, in discovery order
        self.sections = [os.path.basename(root_path)]

    def load(self, filename):
        if filename not in self.schemas:
            with open(os.path.join(self.base_dir, filename)) as fh:
                self.schemas[filename] = json.load(fh)
        return self.schemas[filename]

    def title(self, filename):
        return self.load(filename).get("title", filename)

    def schema_description(self, filename):
        return self.load(filename).get("description")

    def resolve(self, filename, pointer):
        node = self.load(filename)
        for part in filter(None, pointer.split("/")):
            node = node[part]
        return node

    def inline_ref(self, node, current_file):
        """Return the (file, pointer) of the $ref of node inlined in the current table, if any.

        A $ref to the root of another file is not inlined, since it is rendered as own section.
        """
        ref = node.get("$ref")
        if ref is None:
            return None
        filename, pointer = split_ref(ref, current_file)
        if filename != current_file and not pointer:
            return None
        return filename, pointer

    def section_link(self, filename):
        if filename not in self.sections:
            self.sections.append(filename)
        return f"[{self.title(filename)}](#{anchor(filename)})"

    def flatten(self, node, current_file):
        """Flatten inlined $ref and allOf into a single node, returning (node, file)."""
        ref = self.inline_ref(node, current_file)
        node = dict(node)
        if ref is not None:
            del node["$ref"]
            current_file = ref[0]
            target, _ = self.flatten(self.resolve(*ref), current_file)
            node = {**target, **node}
        for sub in node.pop("allOf", []):
            sub, _ = self.flatten(sub, current_file)
            node = {
                **sub,
                **node,
                "properties": {**sub.get("properties", {}), **node.get("properties", {})},
                "required": sub.get("required", []) + node.get("required", []),
            }
        return node, current_file

    def type_label(self, node, current_file):
        if "$ref" in node:
            return self.section_link(split_ref(node["$ref"], current_file)[0])
        if "const" in node:
            return code(node["const"])
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

    def description(self, node, current_file, required, same_as):
        text = node.get("description")
        if not text and "$ref" in node:
            text = self.schema_description(split_ref(node["$ref"], current_file)[0])
        parts = [text] if text else []
        if "enum" in node:
            parts.append("One of " + ", ".join(f"`{v}`" for v in node["enum"]) + ".")
        if "default" in node:
            parts.append(f"Default: {code(node['default'])}.")
        if same_as:
            parts.append(f"Same structure as `{same_as}`, recursively.")
        if required:
            parts.append("**Required.**")
        return escape(" ".join(parts))

    def row(self, depth, label, node, current_file, expanding_refs, required=False):
        """Return a (depth, label, type, description) row for node.

        If node, or the items of node, expands an inlined $ref again, the row points to the field expanding it.
        """
        flat, flat_file = self.flatten(node, current_file)
        refs = [self.inline_ref(node, current_file)]
        if is_array(flat):
            refs.append(self.inline_ref(flat["items"], flat_file))
        same_as = next((expanding_refs[ref] for ref in refs if ref in expanding_refs), None)
        return depth, label, self.type_label(flat, flat_file), self.description(flat, flat_file, required, same_as)

    def rows(self, node, current_file, depth, expanding_refs, parent):
        """Yield the rows for the children of the raw node.

        `expanding_refs` maps the inlined $refs being expanded to the `parent` field expanding them,
        to stop on recursive definitions.
        """
        ref = self.inline_ref(node, current_file)
        if ref in expanding_refs:
            return
        if ref is not None:
            expanding_refs = {**expanding_refs, ref: parent}
        node, current_file = self.flatten(node, current_file)
        if "$ref" in node:
            return
        if is_array(node):
            yield from self.rows(node["items"], current_file, depth, expanding_refs, parent)
            return
        if "oneOf" in node:
            default_variant_title = "variant"
            for variant in node["oneOf"]:
                title = self.flatten(variant, current_file)[0].get("title", default_variant_title)
                # Non-breaking spaces, so a wrapped title does not lose its indentation
                title = title.replace(" ", NBSP)
                yield self.row(depth, f"*{title}*", variant, current_file, expanding_refs)
                yield from self.rows(variant, current_file, depth + 1, expanding_refs, parent)
            return
        required = set(node.get("required", []))
        for name, prop in node.get("properties", {}).items():
            yield self.row(depth, f"`{name}`", prop, current_file, expanding_refs, name in required)
            yield from self.rows(prop, current_file, depth + 1, expanding_refs, name)
        if is_map(node):
            additional = node["additionalProperties"]
            map_key_label = "`<key>`"
            yield self.row(depth, map_key_label, additional, current_file, expanding_refs)
            yield from self.rows(additional, current_file, depth + 1, expanding_refs, parent)

    def table(self, filename):
        indent = NBSP * 4
        lines = ["| Field | Type | Description |", "|---|---|---|"]
        for depth, label, type_, desc in self.rows(self.load(filename), filename, 0, {}, None):
            lines.append(f"| {indent * depth}{label} | {type_} | {desc} |")
        return lines

    def render(self):
        # One level below the heading of the page section including the output
        section_heading = "####"
        out = self.table(self.sections[0])
        # The list iterator also yields the sections appended while rendering
        for filename in itertools.islice(self.sections, 1, None):
            out += ["", f'{section_heading} {self.title(filename)} <a name="{anchor(filename)}"></a>', ""]
            description = self.schema_description(filename)
            if description:
                out += [escape(description), ""]
            out += self.table(filename)
        return "\n".join(out) + "\n"


def main():
    try:
        _, schema, output_path = sys.argv
    except ValueError:
        usage = "Usage: schema_table.py <schema.json> <output.md>"
        sys.exit(usage)
    output = Renderer(schema).render()
    with open(output_path, "w") as fh:
        fh.write(output)


if __name__ == "__main__":
    main()
