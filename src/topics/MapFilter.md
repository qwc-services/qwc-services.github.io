The [`MapFilter`](../references/qwc2_plugins.md#mapfilter) plugin allows filtering the map content via QGIS Server WMS FILTER.

It can be configured to support predefined filters, geometry filters, temporal filters and custom filters, see [`MapFilter`](../references/qwc2_plugins.md#mapfilter).

*Note*: Geometry filters requires the `filter_geom` plugin from [qwc-qgis-server-plugins](https://github.com/qwc-services/qwc-qgis-server-plugins), and the filter will currently only be applied to postgis layers.

You can set predefined filter expressions for a theme item as follows:

```json
"predefinedFilters": [
    {
        "id": "<filter_id>",
        "title": "<filter_title>",
        "titlemsgid": "<filter_title_msgid>",
        "filter": {
            "<layer>": <data_service_filter_expression>
        },
        "fields": [
            {
                "id": "<value_id>",
                "title": "<value_title">,
                "titlemsgid": "<value_title_msgid>",
                "defaultValue": <default_value>,
                "inputConfig": {<input_field_opts>}
            },
            ...
        ]
    },
    ...
]
```

In the data service filter expression, you can use `$<value_id>$` as the value placeholder.

You can specify any common HTML input element properties in `input_field_opts`, i.e.:

```json
"inputConfig": {"type": "number", "min": 0}
```

As a special case, you can define a dropdown list as follows:

```json
"inputConfig": {"type": "select", "options": [{"value": "<value1>", "label|labelmsgid": "<label(msgid)1>"}, ...]}
```

It is also possible to pass a flat list as options, i.e. `["<value1>", "<value2>"]` if the value is equal to the label.

Example:
```json
"predefinedFilters": [{
        "id": "continent_filter",
        "title": "Continent",
        "filter": {
                "countries": ["continent", "=", "$continent$"]
        },
        "fields": [{
                "id": "continent",
                "title": "Name",
                "defaultValue": "",
                "inputConfig": {"type": "select", "options": ["Africa", "Asia", "Europe", "Oceania"]}
        }]
}]
```

The data service filter expressions are of the form `["<name>", "<op>", <value>]`, you can also specify complex expressions concatenated with `and|or` as follows:

```json
[["<name>", "<op>", <value>],"and|or",["<name>","<op>",<value>],...]
```

You can set the startup filter configuration by specifying a `f` URL-parameter with a JSON-serialized string as follows:

```
f={"<filter_id>": {"<field_id>": <value>, ...}, ...}
```

To control the temporal filter, the filter ID is `__timefilter`, and the field IDs are `tstart` and `tend`, with values an ISO date or datetime string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`).

To control the spatial filter, the syntax is `"__geomfilter": <GeoJSON polygon coodinates array>`.

To specify custom filters, the syntax is `"__custom": [{"title": "<title>", "layer": "<layername>", "expr": <JSON filter expr>}, ...]`.

Whenever an startup filter value is specified, the filter is automatically enabled.

*Note*: When specifying `f`, you should also specify `t` as the startup filter configuration needs to match the filters of the desired theme.
