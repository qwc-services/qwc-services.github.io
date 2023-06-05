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
    const crs = "EPSG:XXXX";
    const hidemarker = <boolean>; // Whether to suppress displaying a search marker on top of the search geometry
    callback({geometry: wktString, crs: crs, hidemarker: hidemarker});
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
  cfgParams: <params> // Additional parameters passed in the theme search provider configuration, see below
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
Consult [js/SearchProviders.js](https://github.com/qgis/qwc2-demo-app/blob/master/js/SearchProviders.js) and [static/assets/searchProviders.js](https://github.com/qgis/qwc2-demo-app/blob/master/static/assets/searchProviders.js) for full examples.

## Configuring theme search providers

For each theme item in `themesConfig.json`, you can define a list of search providers to enable for the theme as follows:
```json
...
searchProviders: [
  "<providerkey1>",             // Simple form
  {                             // Provider with custom params
    key: "<providerkey2>",
    params: {
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
Note: The `qwc2-demo-app` (also used by the `qwc-map-viewer-demo` docker image) includes two providers by default: `coordinates` and `nominatim` (OpenStreetMap location search).

## Configuring the fulltext search service <a name="fulltext-search"></a>

For more information on the full-text search provider, see [qwc-fulltext-search-service](https://github.com/qwc-services/qwc-fulltext-search-service).
