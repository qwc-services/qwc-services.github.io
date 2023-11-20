# Search

QWC2 can be configured to use arbitrary custom search providers. In addition, the `qwc-fulltext-search-service` provided by the qwc-services ecosystem can be used.

## Adding search providers

Search providers can be defined as follows:

- Built-in, defined in `js/SearchProviders.js`. This file is structured as follows:
```js
export const SearchProviders = {
    <providerkey1>: <ProviderDefinition1>,
    <providerkey2>: <ProviderDefinition2>,
    ...
};
```
  Built-in search providers are compiled into the application bundle and avoid the need for an extra resource to be loaded on application startup. The downside is that you need to rebuild QWC2 to add/modify search providers.

- As resource, defined in `static/assets/searchProviders.js`. This file is structured as follows:
```js
window.QWC2SearchProviders = {
    <providerkey1>: <ProviderDefinition1>,
    <providerkey2>: <ProviderDefinition2>,
    ...
};
```
  This script file needs to be loaded explicitly by `index.html` via
```html
<script type="text/javascript" src="assets/searchProviders.js" ></script>
```
The format of `ProviderDefinition` is
```js
{
  label: "<human readable provider name>", // OR
  labelmsgid: "<translation message ID for human readable provider name>",
  onSearch: function(searchText, searchParams, callback, axios) => {
    const results = []; // See below
    /* Populate results... */
    callback({results: results});
  },
  getResultGeometry: function(resultItem, callback, axios) => {
    /* Retreive geometry... */
    // resultItem is a search result entry as returned by onSearch, which provides the context for retreiving the geometry
    const geometry = "<wktString>";
    // or
    const geometry = {<GeoJSON geometry>};

    const crs = "EPSG:XXXX";
    const hidemarker = <boolean>; // Whether to suppress displaying a search marker on top of the search geometry
    callback({geometry: geometry, crs: crs, hidemarker: hidemarker});
  },
  handlesGeomFilter: <boolean>; // Hint whether provider will completely filter the results on provider side and that no client-side filtering is necessary
}
```
*Notes:*

* The format of `searchParams` is
```js
{
  displaycrs: "EPSG:XXXX", // Currently selected mouse coordinate display CRS
  mapcrs: "EPSG:XXXX", // The current map CRS
  lang: "<code>", // The current application language, i.e. en-US or en
  cfgParams: <params> // Additional parameters passed in the theme search provider configuration, see below
  filterBBox: <[xmin, ymîn, xmax, ymax]|null> // A filter bbox, in mapcrs, the search component may pass to the provider to narrow down the results
  filterPoly: <[[x0, y0], [x1, y1], ....]> // A filter polygon, in mapcrs, the search component may pass to the provider to narrow down the results
}
```
* `axios` is passed for convenience so that providers can use the compiled-in `axios` library for network requests.

* The format of the `results` list returned by `onSearch` is as follows:
```js
results = [
  {
    id: "<categoryid>",                   // Unique category ID
    title: "<display_title>",             // Text to display as group title in the search results
    priority: priority_nr,                // Optional: search result group priority. Groups with higher priority are displayed first in the list.
    items: [
      {                                   // Location search result:
        type: SearchResultType.PLACE,     // Specifies that this is a location search result
        id: "<itemId">,                   // Unique item ID
        text: "<display text>",           // Text to display as search result
        label: "<map marker text>",       // Optional, text to show next to the position marker on the map instead of `text`
        x: x,                             // X coordinate of result
        y: y,                             // Y coordinate of result
        crs: crs,                         // CRS of result coordinates and bbox
        bbox: [xmin, ymin, xmax, ymax]    // Bounding box of result (if non-empty, map will zoom to this extent when selecting result)
        geometry: <GeoJSON geometry>      // Optional, result geometry. Note: geometries may also be fetched separately via getResultGeometry.
      },
      {                                    // Theme layer search result (advanced):
        type: SearchResultType.THEMELAYER, // Specifies that this is a theme layer search result
        id: "<itemId">,                    // Unique item ID
        text: "<display text>",            // Text to display as search result
        layer: {<Layer definition>}        // Layer definition, in the same format as a "sublayers" entry in themes.json.
      }
    ]
  },
  {
    ...
  }
]
```
* If the provider does not fully handle the filter geometry internally (`handlesGeomFilter != true`), client-side filtering will be performed as follows:

   1. Polygon intersection test if the result has a `geometry` field with a `Polygon` geometry
   2. Polygon intersection test if the result has a `bbox` field
   3. Point-in-polygon test using the results `x` and `y` point coordinates

* Geometry filters are only supported using the `SearchBox` search component with `allowSearchFilters: true` passed in the `TopBar` `searchOptions`.

Consult [js/SearchProviders.js](https://github.com/qgis/qwc2-demo-app/blob/master/js/SearchProviders.js) and [static/assets/searchProviders.js](https://github.com/qgis/qwc2-demo-app/blob/master/static/assets/searchProviders.js) for full examples.

## Configuring theme search providers

For each theme item in `themesConfig.json`, you can define a list of search providers to enable for the theme as follows:
```json
...
searchProviders: [
  "<providerkey1>",             // Simple form
  {                             // Provider with custom params
    "provider": "<providerkey2>",
    "params": {
      ...                       // Arbitrary params passed to the provider `onSearch` function as `searchParams.cfgParams`
    }
  },
  {                             // Fulltext search configuration using qwc-fulltext-search-service
    "provider":"solr",          // Identifier for solr search provider
    "default":[<default terms>] // Default search terms, concatenated with additional search terms from visible theme layers
  }
],
...
```
Note: The `qwc2-demo-app` (also used by the `qwc-map-viewer-demo` docker image) includes three providers by default: `coordinates`, `nominatim` (OpenStreetMap location search), and `qgis` (see <a href="#qgis-search">below</a>).

## Configuring tĥe QGIS feature search <a name="qgis-search"></a>

The QGIS feature search relies on WMS GetFeatureInfo with the [`FILTER`](https://docs.qgis.org/latest/en/docs/server_manual/services/wms.html#wms-filter) parameter to search features of layers which are part of the theme WMS. It is enabled via the `qgis` search provider, which is part of the `qwc2-demo-app`.

In it's simples form, you can configure the theme search provider entry as follows:

```json
  {
    "provider": "qgis",
    "params": {
      "title": "<search name>",
      "expression": {
        "<layername1>": "<expression>",
        "<layername2>": "<expression>"
      }
    }
  }
```

where `expression` is a WMS GetFeatureInfo `FILTER` expression, for example `"\"name\" ILIKE '%$TEXT$%'"`. `$TEXT$` will be replaced by the search text entered by the user, `name` corresponds to a field name of the specified layer.

A more complex form, useable through the [`FeatureSearch`](../references/qwc2_plugins.md#featuresearch) plugin, allows defining a field configuration for multiple input fields. A full example is as follows:

```json
  {
    "provider": "qgis",
    "params": {
      "title": "Person search",
      "expression": {
        "persons": "\"name\" ILIKE '%$NAME$%' AND \"age\" >= $AGE$ AND \"gender\" = '$GENDER$'"
      },
      "fields": {
        "NAME": {"label": "Name", "type": "text"},
        "AGE": {"label": "Min. age", "type": "number", "options": {"min": 0}},
        "GENDER": {"label": "Gender", "type": "select", "options": [{"value": "f", "label": "Female"}, {"value": "m", "label": "Male"}]}
      }
    }
  }
```

Here, each field will provide a value which is substituted in the expression. Any [HTML Input](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) type is supported (i.e. `text`, `number`, `range`, ...), with options depending on the input type. In addition, the `select` field type is supported to display a ComboBox, with the entries provided as `options` as in the example above. It is also possible to pass a flat list as `options`, i.e. `["Female", "Male"]` if the value is equal to the label.

*Note*: `qgis` provider searches are exposed to the search field only if no `fields` are specified (i.e. single input search). The `FeatureSearch` plugin on the other hand will list all `qgis` provider searches.

In addition to the configuration described above, you can specify these additional parameters in `params`:

* `featureCount`: A number, passed as `feature_count` to the GetFeatureInfo request to control the maximum number of returned features. If not specified, defaults to `100`.
* `resultTitle`: A format string for the result title. Allowed placeholders are: `{layername}` for the layer name and `{<fieldname>}` for the value of `fieldname`. If not the layer name followed by the feature displayfield will be shown.
* `description`: An arbitrary descriptive text which will be displayed above the search fields in the `FeatureSearch` plugin.
* `default`: Whether the search is selected by default when opening the `FeatureSearch` plugin.
* `group`: A group name, used to group the searches in the `FeatureSearch` selection combobox.

## Configuring the fulltext search service <a name="fulltext-search"></a>

### Solr configuration

Before the fulltext search service can be configured, a new solr configuration file must be created.
This file must be created in `volumes/solr/configsets/gdi/conf/`.
The name of the file can be chosen freely.
Here is an example XML file:

```xml
<dataConfig>
    <dataSource
        driver="org.postgresql.Driver"
        url="jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
        user="{DB_USER}"
        password="{DB_PASSWORD}"
    />
    <document>
        <entity name="{SEARCH_NAME}" query="
            WITH index_base AS (
                /* ==== Base query for search index ==== */
                SELECT
                    '{SEARCH_NAME}'::text AS subclass,
                    {PRIMARY_KEY} AS id_in_class,
                    '{PRIMARY_KEY}' AS id_name,
                    '{SEARCH_FIELD_DATA_TYPE}:n' AS id_type,
                    {DISPLAYTEXT} AS displaytext,
                    {SEARCH_FIELD_1} AS search_part_1,
                    {GEOMETRY_FIELD} AS geom
                FROM {SCHEMA}.{SEARCH_TABLE_NAME}
                /* ===================================== */
            )
            SELECT
                (array_to_json(array_append(ARRAY[subclass::text], id_in_class::text)))::text AS id,
                displaytext AS display,
                search_part_1 AS search_1_stem,
                search_part_1 AS sort,
                subclass AS facet,
                'default' AS tenant,
                (array_to_json(array_append(ARRAY[id_name::text], id_type::text)))::text AS idfield_meta,
                (st_asgeojson(st_envelope(geom), 0, 1)::json -> 'bbox')::text AS bbox,
                st_srid(geom) as srid
            FROM index_base">
        </entity>
    </document>
</dataConfig>
```

The next table shows how the values need to be defined:

| **Name**                 | **Definition**                                                                    | **Example**      |
|--------------------------|-----------------------------------------------------------------------------------|------------------|
| `DB_HOST`                | Database hostname                                                                 | `qwc-postgis`    |
| `DB_NAME`                | Database name                                                                     | `qwc_demo`       |
| `DB_PORT`                | Database port number                                                              | `5432`           |
| `DB_USER`                | Database username                                                                 | `qwc_service`    |
| `DB_PASSWORD`            | Password for the specified database user                                          | `qwc_service`    |
| `SEARCH_NAME`            | Name of the search                                                                | `fluesse_search` |
| `PRIMARY_KEY`            | Primary key name of the table that is used in the search query                    | `ogc_fid`        |
| `SEARCH_FIELD_DATA_TYPE` | Search field data type                                                            | `str`            |
| `DISPLAYTEXT`            | Displaytext that will be shown by the QWC2 when a match was found                 | `name_long`      |
| `SEARCH_FIELD_1`         | Table field that will be used by the search                                       | `name_long`      |
| `GEOMETRY_FIELD`         | Name of the geometry column of the search table                                   | `wkb_geometry`   |
| `SCHEMA`                 | Search table schema                                                               | `qwc_geodb`      |
| `SEARCH_TABLE_NAME`      | Search table name                                                                 | `fluesse`        |

*Note*:
In the case of several searches sharing the same database connection,
all searche queries can be written to the same XML file. Each search
corresponds to exactly one `<entity>` tag in the XML file.

After the configuration file has been created, the search must be registered in `solr`.
In the `volumes/solr/configsets/gdi/conf/solrconfig.xml` file you have to look for
`<!-- SearchHandler` and add the following configuration

```xml
<requestHandler name="/SEARCH_NAME" class="solr.DataImportHandler">
    <lst name="defaults">
        <str name="config">NAME_OF_THE_CONFIGURATION_FILE.xml</str>
    </lst>
</requestHandler>
```

Finally, the `solr` index has to be generated:

```
rm -rf volumes/solr/data/*
docker compose restart qwc-solr
curl 'http://localhost:8983/solr/gdi/SEARCH_NAME?command=full-import'
```

### Configure fulltext service

The configuration of the fulltext search service can be found in `tenantConfig.json`.
Search the `services` list for the JSON object that has `search` as its name.
Then add a new facet to the facets list. An example entry could be:

```json
{
    "name": "search",
    "config": {
        "solr_service_url": "http://qwc-solr:8983/solr/gdi/select",
        "search_result_limit": 50,
        "db_url": "postgresql:///?service=qwc_geodb"
    },
    "resources": {
        "facets": [
            {
                "name": "SEARCH_NAME",
                "filter_word": "OPTIONAL_SEARCH_FILTER",
                "table_name": "SCHEMA.SEARCH_TABLE_NAME",
                "geometry_column": "GEOMETRY_FIELD",
                "search_id_col": "PRIMARY_KEY"
            }
        ]
    }
}
```

The `filter_word` field can be specified to activate / deactivate searches,
if you have configure multiple searches for one theme.
Normally `filter_word` is left empty (`""`) which results in the search always
being active.
But if specified (e.g. `"house_no"`) then the fulltext search will only use
the configured search, if the user prefixes his search text with `"house_no:"`.

### Activate search for a theme

As a final step, you have to configure the search for the desired themes and give the users the necessary rights in the Admin GUI.

1. Add the following to a theme item in `themesConfig.json`:

```json
"searchProviders": [
    {
        "provider": "solr",
        "default": [<SEARCH_NAME>],
        "layers": {
            "<layer_name>": "<SEARCH_NAME>"
        }
    }
]
```

When activating a search to a theme, you can either:

* Add the search name to the `default` list, resulting in the search always being active.
* Add the search name to the `layers` object, resulting in the search being active only if the theme layer `<layer_name>` is present in the theme.

2. Create a new resource in the Admin GUI

![Create resource](../images/create_solr_search_facet_resource.png?style=centerme)

3. Add permissions on the newly created resource

![Add permission](../images/add_solr_search_facet_permission.png?style=centerme)

4. Re-generate the services configurations with the `Generate service configuration` button

![Generate service configurations](../images/generate_service_configurations.png?style=centerme)
