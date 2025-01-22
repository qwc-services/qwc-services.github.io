# Search

QWC2 can be configured to use arbitrary custom search providers. In addition, the `qwc-fulltext-search-service` provided by the qwc-services ecosystem can be used.

## Adding search providers

Search providers can be defined as follows:

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

- Built-in, defined in `js/SearchProviders.js`. This file is structured as follows:
```js
window.QWC2SearchProviders = {
    <providerkey1>: <ProviderDefinition1>,
    <providerkey2>: <ProviderDefinition2>,
    ...
};
```
  This file needs to be imported into the application, i.e. via
```js
  import './SearchProviders.js';
```
  in `js/appConfig.js`.

  Built-in search providers are compiled into the application bundle and avoid the need for an extra resource to be loaded on application startup. The downside is that you need to rebuild QWC2 to add/modify search providers.

The format of `ProviderDefinition` is
```js
{
  label: "<label>", // Provider label (displayed in provider selection menu)
  labelmsgid: "<msgid>", // Translateable label message ID, instead of `label`
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
    // or
    callback({feature: geojson_feature, crs: crs, hidemarker: hidemarker});
  },
  handlesGeomFilter: <boolean>, // Hint whether provider will completely filter the results on provider side and that no client-side filtering is necessary
  getLayerDefinition: function(resultItem, callback, axios) => {
    // layer definition, in the same format as a "sublayers" entry in themes.json
    const layer = {<layer_definition>};
    callback(layer);
  }
  }
}
```
*Notes:*

* The format of `searchParams` is
```js
{
  displaycrs: "EPSG:XXXX", // Currently selected mouse coordinate display CRS
  mapcrs: "EPSG:XXXX", // The current map CRS
  lang: "<code>", // The current application language, i.e. en-US or en
  cfgParams: <params>, // Additional parameters passed in the theme search provider configuration, see below
  limit: <number>, // Result count limit
  activeLayers: ["<layername>", ...], // List of active layers in the map
  filterBBox: [xmin, ymin, xmax, ymax]|null, // A filter bbox, in mapcrs, the search component may pass to the provider to narrow down the results
  filterPoly: [[x0, y0], [x1, y1], ....], // A filter polygon, in mapcrs, the search component may pass to the provider to narrow down the results
}
```
* `axios` is passed for convenience so that providers can use the compiled-in `axios` library for network requests.

* The format of the `results` list returned by `onSearch` is as follows:
```js
results = [
  {
    id: "<categoryid>",                        // Unique category ID
    title: "<display_title>",                  // Text to display as group title in the search results
    titlemsgid: "<display_title_msgid>",       // Translation message id for group title, instead of "title"
    resultCount: <result_count>,               // Optional: true result count (i.e. not limited to the "limit" specified in searchParams).
    priority: priority_nr,                     // Optional: search result group priority. Groups with higher priority are displayed first in the list.
    type: SearchResultType.{PLACE|THEMELAYER}, // Specifies the type of results. Default: SearchResultType.PLACE
    items: [
      // PLACE result
      {
        id: "<item_id>",                       // Unique item ID
        text: "<display_text>",                // Text to display as search result
        label: "<map_marker_text>",            // Optional, text to show next to the position marker on the map instead of `text`
        x: x,                                  // X coordinate of result
        y: y,                                  // Y coordinate of result
        crs: crs,                              // CRS of result coordinates and bbox. If not specified, the current map crs is assumed.
        bbox: [xmin, ymin, xmax, ymax],        // Bounding box of result (if non-empty, map will zoom to this extent when selecting result)
        geometry: <GeoJSON geometry>,          // Optional, result geometry. Note: geometries may also be fetched separately via getResultGeometry.
        thumbnail: "<thumbnail_url>",          // Optional: thumbnail to display next to the search result text in the result list,
        externalLink: "<url>"                  // Optional: a url to an external resource. If specified, a info icon is displayed in the result entry to open the link.
        target: "<target>"                     // Optional: external link target, i.e. _blank or iframe
      },
      // THEMELAYER result
      {
        id: "<item_id>",                        // Unique item ID
        text: "<display_text>",                 // Text to display as search result
        layer: {<layer_definition>}             // Optional: layer definition, in the same format as a "sublayers" entry in themes.json. Layer definitions may also be fetched separately via getLayerDefinition.
        info: <bool>,                           // Optional: Whether to display a info icon in the result list. The info is read from layer.abstract. If layer is not specified, the layer is fecthed via getLayerDefinition.
        thumbnail: "<thumbnail_url>",           // Optional: thumbnail to display next to the search result text in the result list,
        sublayers: [{<sublayer>}, ...]          // Optional: list of sublayers, in the format {id: "<item_id>", text: "<display_text>", has_info: <bool>, etc..}
      }
    ]
  }
]
```

Consult [static/assets/searchProviders.js](https://github.com/qgis/qwc2-demo-app/blob/master/static/assets/searchProviders.js) for a full examples.

## Filtering <a name="filtering"></a>

When using the `SearchBox` search component with `allowSearchFilters: true` passed in the `TopBar` `searchOptions`, you a filter menu will be displayed allowing to restrict the search area.

If the provider does not fully handle the filter geometry internally (`handlesGeomFilter != true`), client-side filtering will be performed as follows:

1. Polygon intersection test if the result has a `geometry` field with a `Polygon` geometry
2. Polygon intersection test if the result has a `bbox` field
3. Point-in-polygon test using the results `x` and `y` point coordinates

You can also set a predefined list of filter areas by setting `searchFilterRegions` in `config.json` (or per-theme in `themesConfig.json`) as follows:
```json
"searchFilterRegions": [
  {
    "name": "<Group name>",
    "items": [
      {
        "name": "<Name>",
        "crs": "<EPSG:XXXX>",
        "coordinates": [[x0, y0], [x1, y1], ...]
      },
      ...
    ]
  },
  ...
]
 ```

## Configuring theme search providers

For each theme item in `themesConfig.json`, you can define a list of search providers to enable for the theme as follows:
```json
...
searchProviders: [
  "<providerkey1>",             // Simple form
  {                             // Provider with custom params
    "provider": "<providerkey2>",
    "key": "<key>",             // Optional: key to disambiguate multiple provider configurations of the same provider type (i.e. multiple `qgis` provider configurations)
    "label": "<label>",         // Optional: provider label (displayed in provider selection menu). If not specified, the label/labelmsgid from the provider definition is used.
    "labelmsgid": "<msgid>",    // Optional: translateable label message ID, instead of `label`
    "params": {
      ...                       // Additional params passed to the provider `onSearch` function as `searchParams.cfgParams`
    }
  }
]
...
```
Note: The `qwc2-demo-app` (also used by the `qwc-map-viewer-demo` docker image) includes four providers by default: `coordinates`, `nominatim` (OpenStreetMap location search), `qgis` (see <a href="#qgis-search">below</a>) and `fulltext` (see <a href="#fulltext-search">below</a>).

## Configuring the QGIS feature search <a name="qgis-search"></a>

The QGIS feature search relies on WMS GetFeatureInfo with the [`FILTER`](https://docs.qgis.org/latest/en/docs/server_manual/services/wms.html#wms-filter) parameter to search features of layers which are part of the theme WMS. It is enabled via the `qgis` search provider, which is part of the `qwc2-demo-app`.

*Note*: Make sure the QGIS Project is configured to return geometries with the feature info responses (`Project` &rarr; `Properties` &rarr; `QGIS Server` &rarr; `Add geometry to feature response`).

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

The [`qwc-fulltext-search-service`](https://github.com/qwc-services/qwc-fulltext-search-service) provides facetted fullsearch text search, with one of the following backends:

* Postgres Trigram
* Apache Solr

A facet references a searchable dataset. The configuration of the fulltext search service and available search facets can be found in `tenantConfig.json`:

```json
{
    "name": "search",
    "config": {
        "search_backend": "<solr|trgm>",
        "word_split_re": "[\\s,.:;\"]+",
        "search_result_limit": 50,
        "db_url": "postgresql:///?service=qwc_geodb",
        // trgm specific configuration, see below
        "trgm_feature_query": "<see below>",
        "trgm_feature_query_template": "<see below>",
        "trgm_layer_query": "<see below>",
        "trgm_layer_query_template": "<see below>",
        "trgm_similarity_threshold": "0.3"
        // solr specific configuration, see below
        "solr_service_url": "http://localhost:8983/solr/gdi/select",
        "search_result_sort": "score desc, sort asc",
    },
    "resources": {
        "facets": [
            {
                "name": "<facet name>",
                "filter_word": "<filter word>",
                "table_name": "<schema.tablename>",
                "geometry_column": "<geometry column name>",
                "search_id_col": "<id column name>"
            },
            ...
        ]
    }
}
```

- The `search_backend` specifies the search backend to use, either `solr` or `trgm`. Default: `solr`.
- The `db_url` specifies the DB which contains the search index (searched either by `solr` or by the specified `trgm` queries).
- The `word_split_re` specifies the regular expression which is used to split the search string into single words. Default: `[\\s,.:;\"]+`.
- `search_result_limit` specifies the maximum number of feature results returned by a search. Default: `50`.

The facets describe a searchable dataset and are referenced by the search index:

- `name` specifies the facet identifier.
- `filter_word` is a short (human readable) name which appears as result category in the search results (i.e. `Address`).
- `table_name` specifies the table containing the features referenced by the search index (in the format `schema.table_name`).
- `geometry_column` specifies the name of the geometry column in this table.
- `search_id_col` specifies the name of the id column in this table. If unset, field from search filter expression is used.


### Fulltext search with Trigram backend

To configure a fulltext search with the trigram backend, set `search_backend` to `trgm` and specify a `trgm_feature_query` and optionally a `trgm_layer_query`. The feature and layer query SQL can contain following placeholders:

- `:term`: The full search text
- `:terms`: A list of search text words (i.e. the full search text split by whitespace).
- `:thres`: The trigram similarity treshold value (note that the service will also separately execute `SET pg_trgm.similarity_threshold = <value>`)

The `trgm_feature_query` must return the following fields:

* `display`: The label to display in the search results.
* `facet_id`: The facet name (as configured in `resources` => `facets`).
* `id_field_name`: The name of the identifier field in the table referenced by the facet.
* `feature_id`: The feature identifier through which to locate the feature in table referenced by the facet.
* `bbox`: The feature bounding box, as a`[xmin,ymin,xmax,ymax]` string.
* `srid`: The SRID of the bbox coordinates (i.e. `3857`).

Example:

    SELECT display, facet_id, id_field_name, feature_id, bbox, srid, similarity(suchbegriffe, :term) sml
    FROM public.search_index WHERE searchterms % :term OR searchterms ILIKE '%' || :term || '%' ORDER BY sml DESC;",

The `trgm_layer_query` must return the following fields:

* `display`: The label to display in the search results.
* `dataproduct_id`: The id of the dataproduct.
* `has_info`: Whether an abstract is available for the dataproduct.
* `sublayers`: A JSON stringified array of the shape `[{"ident": "<dataproduct_id>", "display": "<display>", "dset_info": true}, ...]`, or `NULL` if no sublayers exist.

*Note*: The layer query relies on an additional service, configured as `dataproductServiceUrl` in the viewer `config.json`, which resolves the `dataproduct_id` to a QWC theme sublayer object, like the [`sogis-dataproduct-service`](https://github.com/qwc-services/sogis-dataproduct-service).

In alternative to specifying `trgm_feature_query` and/or `trgm_layer_query`, you can set `trgm_feature_query_template` and/or `trgm_layer_query_template` to a [Jinja template string](https://jinja.palletsprojects.com/en/stable/templates/) which generates the final SQL query. The following variables are available in the template string:

* `searchtext`: the full search text, as a string
* `words`: the single words of the search text, as an array
* `facets`: the permitted search facets, as an array

Example for `trgm_feature_query_template` to generate an "unrolled" query for each word in the searchtext:

    SELECT display, facet_id, id_field_name, feature_id, bbox, srid FROM public.search_index
    WHERE {% for word in words %} searchterms ILIKE '%' || '{{ word }}' || '%' {% if not loop.last %} AND {% endif %} {% endfor %}
    ORDER BY {% for word in words %} similarity(searchterms, '{{ word }}') {% if not loop.last %} + {% endif %} {% endfor %} DESC

*Note*: Set `FLASK_DEBUG=1` as environment variable for the search service to see additional logging information.

### Fulltext search with Solr backend

To use the solr backend, you need to run a solr search service and point `solr_service_url` to the corresponding URL. You can find the solr documentation at [https://lucene.apache.org/solr/guide/8_0/](https://lucene.apache.org/solr/guide/8_0/).

Next, create search XML configuration files in `volumes/solr/configsets/gdi/conf/`. The name of the file can be chosen freely. Example:

```xml
<dataConfig>
    <dataSource
        driver="org.postgresql.Driver"
        url="jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
        user="{DB_USER}"
        password="{DB_PASSWORD}"
    />
    <document>
        <entity name="{FACET_NAME}" query="
            WITH index_base AS (
                /* ==== Base query for search index ==== */
                SELECT
                    '{FACET_NAME}'::text AS subclass,
                    {PRIMARY_KEY} AS id_in_class,
                    '{PRIMARY_KEY}' AS id_name,
                    'str:{SEARCH_FIELD_IS_STRING}' AS search_field_str,
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
                (array_to_json(array_append(ARRAY[id_name::text], search_field_str::text)))::text AS idfield_meta,
                (st_asgeojson(st_envelope(geom), 0, 1)::json -> 'bbox')::text AS bbox,
                id_name,
                geom
            FROM index_base">
        </entity>
    </document>
</dataConfig>
```

The next table shows how the values need to be defined:

| **Name**                 | **Definition**                                                                                 | **Example**      |
|--------------------------|------------------------------------------------------------------------------------------------|------------------|
| `DB_HOST`                | Database hostname                                                                              | `qwc-postgis`    |
| `DB_NAME`                | Database name                                                                                  | `qwc_demo`       |
| `DB_PORT`                | Database port number                                                                           | `5432`           |
| `DB_USER`                | Database username                                                                              | `qwc_service`    |
| `DB_PASSWORD`            | Password for the specified database user                                                       | `qwc_service`    |
| `FACET_NAME`             | Name of the search facet                                                                       | `fluesse_search` |
| `PRIMARY_KEY`            | Primary key name of the table that is used in the search query                                 | `ogc_fid`        |
| `SEARCH_FIELD_IS_STRING` | Definition, if search field is string (`y`) or not (`n`). If not, it's interpreted as integer. | `n`              |
| `DISPLAYTEXT`            | Displaytext that will be shown by the QWC2 when a match was found                              | `name_long`      |
| `SEARCH_FIELD_1`         | Table field that will be used by the search                                                    | `name_long`      |
| `GEOMETRY_FIELD`         | Name of the geometry column of the search table                                                | `wkb_geometry`   |
| `SCHEMA`                 | Search table schema                                                                            | `qwc_geodb`      |
| `SEARCH_TABLE_NAME`      | Search table name                                                                              | `fluesse`        |

**Hint**: For a less complex configuration file, of course it is also possible to define the query within a `VIEW` definition within the database. In this case just provide the query within the facet configuration like:
```xml
<entity name="{FACET_NAME}" query="
    SELECT id,
    display,
    search_1_stem,
    sort,
    facet,
    tenant,
    idfield_meta,
    bbox
    id_name,
    geom
    FROM index_base">
</entity>
```

*Note*:
In the case of several searches sharing the same database connection,
all searche queries can be written to the same XML file. Each search
corresponds to exactly one `<entity>` tag in the XML file.

After the configuration file has been created, the search must be registered in `solr`.
In the `volumes/solr/configsets/gdi/conf/solrconfig.xml` file you have to look for
`<!-- SearchHandler` and add the following configuration

```xml
<requestHandler name="/FACET_NAME" class="solr.DataImportHandler">
    <lst name="defaults">
        <str name="config">NAME_OF_THE_CONFIGURATION_FILE.xml</str>
    </lst>
</requestHandler>
```

Finally, the `solr` index has to be generated:

```
rm -rf volumes/solr/data/*
docker compose restart qwc-solr
curl 'http://localhost:8983/solr/gdi/FACET_NAME?command=full-import'
```


### Configuring the search for a theme

To use a fulltext search in a theme, configure a `fulltext` search provider in `themesConfig.json` as follows:

```json
"searchProviders": [
    {
        "provider": "fulltext",
        "params": {
          "default": [<FACET_NAME>],
          "layers": {
              "<layer_name>": "<FACET_NAME>"
          }
        }
    }
]
```
Where:

* `default` lists the search facets enabled by default.
* `layers` providides a mapping of facets which are enabled whenever the theme layer `<layer_name>` is visible on the map.

Next, create the resources in the Admin GUI to control the search permissions:

  * For feature results, create `Search facet` resources in the Admin GUI with the facet names you want to permit.
  * For layer results, create `Dataproduct` resources in the Admin GUI with the dataproduct ids you want to permit.

*Note*: For both `Search facet` and `Dataproduct` resources you can create wildcard resources by setting the name to `*`. This is useful to assign permissions for all available facets/dataproducts with one single resource.

Finally, create permissions for the newly created resources and regenerate the service configuration.
