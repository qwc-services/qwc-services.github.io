# Snapping

QWC ships a plugin for snapping support while drawing (redlining / measuring / editing). The plugin is enabled in the stock application. To enable it in a custom application, make sure the `SnappingSupport` plugin is enabled in `appConfig.js` (see the sample [sample `js/appConfig.js`](https://github.com/qgis/qwc2-demo-app/blob/master/js/appConfig.js)). Then, for each theme for which you want snapping to be available, you can add a `snapping` block to your theme item in `themesConfig.json` as follows:
```json
...
"snapping": {
  "snaplayers": [
    {
      "name": "<layername>",
      "min": <min_scale>,
      "max": <max_scale>
    }
  ],
  "featureCount": <feature_count>,
  "wfsMaxScale": <wfs_max_scale>
}
...
```
where:

- `layername` is the name of the theme sublayer from which to retreive the snapping geometries.
- `min` is the minimum scale denominator (inclusive) from which this layer should be used for snapping.
- `max` is the maximum scale denominator (exclusive) up to which this layer should be used for snapping.
- `feature_count` is the maximum number of snapping geometries to retreive for the current map extent (default: 500).
- `wfs_max_scale` is the maximum scale denominator (exclusive) up to which loaded WFS layers should be used for snapping.

*Note*: Snapping works by querying the geometries of all snapping layers inside the scale range via WMS GetFeatureInfo and refreshing the geometries every time the map extent changes. Therefore, it is recommended to ensure the geometry complexity of the snap layers is appropriate for the specified scale ranges to avoid overloading the server with the GetFeatureInfo requests. Also, the QGIS project will need to be configured so that snap layers are queryable and that feature info responses contain geometries.

For the `Redlining`, `Measure` and `Editing` plugins, the availability of snapping can be independently configured:
```json
{
  "name":"<Redlining|Measure|Editing>",
  "cfg": {
    "snapping": <true|false>,
    "snappingActive": <true|false>,
    ...
  }
}
```
where:

- `snapping` determines whether snapping is available for the specified plugin
- `snappingActive` determines whether snapping is active by default for the specified plugin

When snapping is available, a small toolbar appears on the bottom border of the map with the possibility to toggle snapping.

