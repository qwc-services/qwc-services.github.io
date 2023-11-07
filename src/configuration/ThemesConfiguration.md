# Themes configuration

A theme corresponds to a QGIS project, published as WMS and served by QGIS Server.

The basic steps for configuring a theme are:

- [Create a QGIS project and deploy it to QGIS Server](#create-qgis-project)
- [Writing the QWC2 theme configuration](#writing-themes-configuration)
- [Generating the themes configuration](#generating-themes-configuration)

## Creating and publishing a QGIS project<a name="create-qgis-project"></a>

The first step is to prepare a QGIS project for publishing. Besides the common tasks of adding and styling layers, the following table gives an overview of settings which influence how the theme is displayed in QWC2:

| What                 | Where                                     | Description                                      |
|----------------------|-------------------------------------------|--------------------------------------------------|
| Service Metadata     | Project Properties &rarr; QGIS Server &rarr; Service capabilities | Shown in the theme info dialog, invokable from the Layer Tree panel titlebar. |
| Title, keywords      | Project Properties &rarr; QGIS Server &rarr; Service capabilities | Theme title, displayed in the Theme Switcher, and keywords, useful for filtering. |
| Map extent           | Project Properties &rarr; QGIS Server &rarr; WMS &rarr; Advertised extent | The extent used as initial map extent when loading the theme, unless overridden in `themesConfig.json`. |
| Queryable layers     | Project Properties &rarr; Data sources | Mark layers as identifyable by the client.       |
| FeatureInfo geometry | Project Properties &rarr; QGIS Server &rarr; WMS Capabilities &rarr; Add geometry to feature response | Return feature geometries with the GetFeatureInfo request. Allows the client to highlight the selected features. |
| Layer Display Field  | Vector Layer Properties &rarr; Display    | The field used in the identify results. |
| Layer Map Tip        | Vector Layer Properties &rarr; Display    | The contents of the Map Tip shown when hovering over layers in the client, if displaying Map Tips is enabled in the Layer Tree. |
| Layer Metadata       | Layer Properties &rarr; QGIS Server       | Shown in the client Layer Info dialog, invokable from the Layer Tree. |
| Scale range          | Layer Properties &rarr; Rendering &rarr; Scale dependent visibility | The scale range within which a layer is visible, useful to improve rendering performance. |
| Initial visibility   | Layers Panel                              | Initial visibility of layers and groups.         |
| Rendering order      | Layer Order Panel or Layers Panel         | Rendering order of the layers. If layer re-ordering is enabled in `config.json`, the order from the Layer Order Panel is ignored. |
| Print layouts        | Layout manager                            | The print layouts offered in the Print plugin.   |
| Print layout labels  | Layout manager                            | Print layout labels with an ID will be exposed in the Print plugin. Note: a label ID starting with `__` will not be exposed. |
| Attribute form       | Vector Layer Properties &rarr; Attributes Form | The configured attribute form will be displayed when editing in QWC2. |
| External layers      | Layer Properties &rarr; QGIS Server &rarr; Data URL | Mark the layer as an external layer to avoid cascaded requests. See [Configuring external layers](#external-layers). |

Then, store the project in the publishing directory of your QGIS Server instance. When using `qwc-docker`, store the project as `*.qgs` below `qwc-docker/volumes/qgs-resources`.

Alternatively, when using `qwc-docker`, you can also store the project in a database in QGIS using Project &rarr; Save To &rarr; PostgreSQL (see [Storing projects in database](#projects-in-database)).

### Ensuring valid datasources

A common issue is that the project will reference datasources in locations which cannot be resolved when QGIS Server reads the project, in particular when running QGIS Server inside a docker container. To avoid such issues:

- Make sure that any file-based resources are located on the same level or below the level of the `*.qgs` project file. Remember to copy all resources along with the `*.qgs` project file to the server.
- Load any PostgreSQL datasource in QGIS using a service, and make sure the service definition exists both in the `pg_service.conf` on your host system as well as in the `qwc_docker/pg_service.conf` and `qwc_docker/pg_service-write.conf` which are mounted inside the docker containers. For instance, to use default `qwc-docker` database, use the `qwc_geodb` service and add the service definition to your host `pg_service.conf` as follows:
```
[qwc_geodb]
host=localhost
port=5439
dbname=qwc_demo
user=qwc_service
password=qwc_service
sslmode=disable
```

## Configuring the themes in `themesConfig.json` <a name="writing-themes-configuration"></a>

The next step is to configure the theme for QWC2. There are two approaches:

- [Automatic theme configuration](#automatic-theme-configuration) (only when using `qwc-docker`): Just copy the project file to the designated location and the `qwc-config-generator` will automatically generate a theme configuration using default parameters.
- [Manual theme configuration](#manual-theme-configuration): Manually configure a theme with the full set of configuration options.

### Automatic theme configuration <a name="automatic-theme-configuration"></a>

When using `qwc-docker`, save your QGIS projects below `qwc-docker/volumes/qgs-resources/scan`. Adjust the default settings (`defaultMapCrs`, `defaultBackgroundLayers`, etc.) as desired in `qwc-docker/volumes/config-in/<tentant>/themesConfig.json`. Then [generate the theme configuration](#generating-theme-configuration).

You can configure an automatically configured theme as default theme by setting `defaultTheme` in `themesConfig.json` to the path to the QGIS project file below `qwc-docker/volumes/qgs-resources`, without the `.qgs` extension. For example to set `qwc-docker/volumes/qgs-resources/scan/project.qgs` as default theme, you'd write

    ...
    "defaultTheme": "scan/project"
    ...

To use a custom thumbnail for an automatically configured theme, place a an image called `<project_basename>.png` in `qwc-docker/volumes/qwc2/assets/img/mapthumbs`. For example. if the project is called `project_name.qgs`, the name thumbnail image would be named `project_name.png`.

*Note:* The auto-scan directory can be is controlled by `qgis_projects_scan_base_dir` in `qwc-docker/volumes/config-in/<tentant>/themesConfig.json`.

### Manual theme configuration <a name="manual-theme-configuration"></a>

The theme configuration file is located as follows:

- Standalone viewer: `qwc2-app/themesConfig.json`
- `qwc-docker`: `qwc-docker/volumes/config-in/<tentant>/themesConfig.json`

*Note*: when using `qwc-docker`, the themes configuration may also be embedded as `themesConfig` directly in `qwc-docker/volumes/config-in/<tentant>/tenantConfig.json`.

The `themesConfig.json` file contains a list of themes, optionally organized in groups, as well as a list of background layers:
```json
{
  "themes": {
    "items": [
      { <ThemeDefinition> },
      ...
    ], "groups": [
      {
        "title": <Group title>,
        "items": [{ <ThemeDefinition> }, ...],
        "groups": [ { <Group> }, ...]
        },
        ...
    ],
    "externalLayers": [
      { <ExternalLayerDefinition> },
      ...
    ],
    "themeInfoLinks": [
      { <ThemeInfoLinkDefinition> },
      ...
    ],
    "pluginData": {
      "<PluginName>": [{ <PluginDataReource>}, ...],
      ...
    },
    "backgroundLayers": [
      { <BackgroundLayerDefinition> },
      ...
    ],
  },
  "defaultMapCrs": "<Default map crs, defaults to EPSG:3857>",
  "defaultBackgroundLayers": "<Default background layers, see theme definition below>",
  "defaultWMSVersion": "<Default WMS version, i.e. 1.3.0>",
  "defaultScales": [<Scale denominators, see theme definition below>],
  "defaultPrintScales" [<Scale denominators, see theme definition below>],
  "defaultPrintResolutions": [<DPIs, see theme definition below>],
  "defaultSearchProviders": [<Search providers, see theme definition below>],
  "defaultPrintGrid": [<Print grid, see theme definition below>],
  "defaultTheme": "<Default theme id>"
}
```

Refer to [External layers](#external-layers), [Theme info links](#theme-info-links), [Plugin data](#plugin-data) and [Background layers](#background-layers) for the format of the respective definitions.

Refer to the [sample `themesConfig.json`](https://github.com/qgis/qwc2-demo-app/blob/master/themesConfig.json) for a complete example.

The format of the theme definitions is as follows:
<!-- Important: Use U+00A0 non-breaking spaces ( ) in code blocks -->
| Entry                                           | Description                                                                       |
|-------------------------------------------------|-----------------------------------------------------------------------------------|
| `"id": "<id>",`                                 | Theme identificator. Autogenerated if not specified.                              |
| `"url": "<WMS URL>",`                           | The address of desired WMS served by QGIS Server.                                 |
| `"mapCrs: "<EPSG code>",`                       | Optional, map projection, defaults to `defaultMapCrs`.                            |
| `"title": "<Custom title>",`                    | Optional, override WMS title.                                                     |
| `"description": "<Description>",`               | Optional, an additional description to show below the theme title.                |
| `"thumbnail": "<Filename>",`                    | Optional, image file in `assets/img/mapthumbs` (see [Viewer assets](ViewerConfiguration.md#viewer-asset)). If omitted, `<project_basename>.png` will be used if it exists below `assets/img/mapthumbs`, otherwise it is autogenerated via WMS GetMap. |
| `"attribution": "<Attribution>",`               | Optional, attribution which will be shown in the bottom right corner of the map.  |
| `"attributionUrl": "<URL>",`                    | Optional, link associated to the attribution                                      |
| `"scales": [<Scale denominators>],`             | List of denominators of allowed map scales. If omitted, defaults to `defaultScales`. |
| `"printScales": [<Scale denominators>],`        | List of denominators of allowed print scales. If omitted, defaults to `defaultPrintScales`. |
| `"printResolutions": [<DPIs>],`                 | List of available print resolutions. If omitted, defaults to `defaultPrintResolutions`. |
| `"printGrid": [`                                | List of grid scale-dependent grid intervals to use when printing. If omitted, defaults to `defaultPrintGrid`. |
| `⁣  {"s": <Scale1>, "x": <Width1>, "y": <Height1>},` | Keep this list sorted in descending order by scale denominator.           |
| `⁣  {"s": <Scale2>, "x": <Width2>, "y": <Height2>}`  | In this example, `{x: <Width2>, y: <Height2>}` will be used for `<Scale1> > Scale >= <Scale2>`. |
| `],`                                            |                                                                                  |
| `"printLabelForSearchResult": "<ID>",`          | Optional, an ID of a print layout label to which the current search result text (if any) will be written to when printing. |
| `"printLabelForAttribution": "<ID>",`           | Optional, an ID of a print layout label to which the current attribution text (if any) will be written to when printing. |
| `"printLabelConfig": {`                         | Optional, configuration of the text input fields for print layout labels.        |
| `⁣  "<LabelId>": {`                              |                                                                                  |
| `⁣  ⁣  "defaultValue": "<value">,`                | Optional, default value.                                                         |
| `⁣  ⁣  <textarea config>,`                        | Optional, additional [`textarea` properties](https://react.dev/reference/react-dom/components/textarea), i.e. `maxLength`, `rows`, `placeholder`, ...    |
| `⁣  ⁣  "options": ["<value1>","<value2>",...]`    | Optional, to display a ComboBox with the specified options instead of a free-input textfield. |
| `},`                                            |                                                                                  |
| `"extent": [<xmin>, <ymin>, <xmax>, <ymax>],`   | Optional, override theme extent. In `mapCrs`.                                    |
| `"tiled": <boolean>,`                           | Optional, use tiled WMS, defaults to `false`.                                    |
| `"tileSize": [<tile_width>, <tile_height>]`     | Optional, the WMS tile width and height.                                         |
| `"format": "<mimetype>",`                       | Optional, the format to use for WMS GetMap. Defaults to `image/png`.             |
| `"externalLayers": [{`                          | Optional, external layers to use as replacements for internal layers. |
| `⁣  "name": "<external_layer_name>",`            | Name of the external layer, matching a `ExternalLayerDefinition`, see [below](#external-layers). |
| `⁣  "internalLayer": "<QGis_layer_name>"`        | Name of an internal layer, as contained in the QGIS project, to replace with the external layer. |
| `}],`                                           |                                                                                  |
| `"themeInfoLinks": {`                           | Optional, custom links to additional resources, shown as a menu in the theme selector in the theme switcher.\
| `⁣  "title": "<Menu title>",`                    | An arbitrary string shown as title of the menu.                                  |
| `⁣  "titleMsgId": "<Menu title msgID>",`         | Alternative to `title`, a message ID, translated through the translation files.  |
| `⁣  "entries": ["<link_name>", ...]`             | List of theme info link names, see [below](#theme-info-links).                   |
| `},`                                            |                                                                                  |
| `"backgroundLayers": [{,`                       | Optional, list of available background layers, defaults to `defaultBackgroundLayers`. |
| `⁣  "name": "<Background layer name>",`          | Name of matching `BackgroundLayerDefinition`, see [below](#background-layers).   |
| `⁣  "printLayer": "<layer name>"\|[<list>],`     | Optional, a QGIS layer name or layer resource string to use as matching background layer when printing. Alternatively, a list `[{"maxScale": <scale>, "name": "<layer name>"}, ..., {"maxScale": null, "name": "<layer name>"}]` can be provided, ordered in ascending order by `maxScale`. The last entry should have `maxScale` `null`, as the layer used for all remaining scales. If omitted, no background is printed, unless layer is of type `wms` and `printExternalLayers` is `true` in the Print plugin configuration. See [Printing](../topics/Printing.md). |
| `⁣  "visibility": <boolean>`,                    | Optional, initial visibility of the layer when theme is loaded.                  |
| `⁣  "overview": <boolean>`,                      | Optional, set the layer as the overview map layer (i.e. this layer will be displayed in the overview map regardless of the background layer visible in the main map).                  |
| `}],`                                           |                                                                                  |
| `"searchProviders": ["<Provider>"],`            | Optional, list of search providers, see [Search](../topics/Search.md). Defaults to `defaultSearchProviders`. |
| `"minSearchScaleDenom": <number>,`              | Optional, minimum scale to enforce when zooming to search results. Takes precedence over value in `config.json`. |
| `"featureReport": {`                            | Optional, available feature report templates.                                    |
| `⁣  "<LayerId>": "<TemplateID>"  `               | WMS sublayer ID and associated template ID to pass to the `featureReportService`.|
| `},`                                            |                                                                                  |
| `"additionalMouseCrs": ["<EPSG code>"],`        | Optional, list of additional projections for displaying the mouse position. WGS84 and `mapCrs` are available by default. Additional projections definitions must be added to `config.json`.         |
| `"watermark": {`                                | Optional, configuration of watermark to add to raster export images.             |
| `⁣  "text": "<text>",`                           | Arbitrary text.                                                                  |
| `⁣  "texpadding": <number>,`                     | Optional, padding between text and frame, in points.                             |
| `⁣  "fontsize": <number>,`                       | Optional, font size.                                                             |
| `⁣  "fontfamily": "<Font family>",`              | Optional, font family.                                                           |
| `⁣  "fontcolor": "#RRGGBB",`                     | Optional, font color.                                                            |
| `⁣  "backgroundcolor": "#RRGGBB",`               | Optional, frame background color.                                                |
| `⁣  "framecolor": "#RRGGBB",`                    | Optional, frame color.                                                           |
| `⁣  "framewidth": <number>,`                     | Optional, frame width.                                                           |
| `},`                                            |                                                                                  |
| `"collapseLayerGroupsBelowLevel": <level>,`     | Optional, layer tree level below which to initially collapse groups. By default the tree is completely expanded. |
| `"skipEmptyFeatureAttributes": <boolean>,`      | Optional, whether to skip empty attributes in the identify results. Default is `false`. |
| `"mapTips": <boolean>\|null,`                   | Optional, per-theme setting whether map-tips are unavailable (`null`), disabled by default (`false`) or enabled by default (`true`). |
| `"extraLegendParameters": "<&KEY=VALUE>",`      | Optional, [additional query parameters](https://docs.qgis.org/latest/en/docs/server_manual/services/wms.html#getlegendgraphics) to append to GetLegendGraphic request.     |
| `"extraDxfParameters": "<&KEY=VALUE>",`         | Optional, [additional query parameters](https://docs.qgis.org/latest/en/docs/server_manual/services/wms.html?highlight=dxf#format-options) to append to DXF export request.           |
| `"extraPrintParameters": "<&KEY=VALUE>",`       | Optional, additional query parameters to append to GetPrint request (requires QGIS Server >= 3.32.0). |
| `"printLabelBlacklist": ["<LabelId>", ...]`     | Optional, list of composer label ids to not expose in the print dialog.          |
| `"editConfig": "<editConfig.json>"`             | Optional, object or path to a filename containing the editing configuration for the theme, see [Editing](#editing). |
| `"snapping": {...},`                            | Optional, snapping configuration, see [Snapping](#snapping). |                   |
| `"config": {`                                   | Optional, per-theme configuration entries which override the global entries in `config.json`, see [Viewer Configuration](ViewerConfiguration.md).|
| `⁣  "allowRemovingThemeLayers": <boolean>`       | See [`config.json`](ViewerConfiguration.md#theme-overridable-settings) for which settings can be specified here. |
| `⁣  ...`                                         |                                                                                  |
| `}`                                             |
| `"pluginData": {`                               | Optional, data to pass to custom plugins.                                        |
| `⁣  "<PluginName>": ["<plugin_data_resource_name>"],`| A list of plugin resource names for the specified plugin. See [below](#plugin-data). |
| `⁣  ...`                                         |                                                                                  |
| `},`                                            |                                                                                  |
| `"wmsBasicAuth": "{`                            | Optional, allows to authenticate to QGIS Server during themes.json generation. NOTE: these credentials will solely be used by `yarn run themesConfig` and won't be stored in `themes.json`.|
| `⁣  "username": <username>`                      | Optional: http basic authentication username.                                    |
| `⁣  "password": <password>`                      | Optional: http basic authentication password.                                    |
| `},`                                            |                                                                                  |

A bare minimum theme entry might look as follows:
```json
{
  "id": "theme_id",
  "title": "My theme",
  "url": "/ows/my_theme",
  "mapCrs": "EPSG:3857",
  "backgroundLayers": [{"name": "background_layer_name"}],
  "searchProviders" ["coordinates"]
}
```
*Note:*

* The theme identifier `id` can be freely defined and will appear in the viewer URL as the `t` query parameter.
* When using `qwc-docker`, the `url` can be specified as `/ows/<relative_path_to_qgs>` where `relative_path_to_qgs` is the path to the QGIS project file below `qwc-docker/volumes/qgs-resources`, without the `.qgs` extension. In the above sample, the project file would be located at `qwc-docker/volumes/qgs-resources/my_theme.qgs`.

### External layers <a name="external-layers"></a>

External layers can be used to selectively replace layers in a QGIS project with a layer from an external source, for instance in the case of a WMS layer embedded in a QGIS project, to avoid cascading WMS requests. They are handled transparently by QWC2 (they are positioned in the layer tree identically to the internal layer they replace), but the `GetMap` and `GetFeatureInfo` requests are sent directly to the specified WMS Service.

**Configuring external layers via Data Url**

The simplest way to define an external layer is to set the "Data Url" for a layer in QGIS (Layer Properties &rarr; QGIS Server &rarr; Data Url) to a string of these forms
```text
wms:<service_url>?<options>#<layername>
wmts:<capabilities_url>?<options>#<layername>
```
For instance:
```text
wms:http://wms.geo.admin.ch?tiled=false&infoFormat=application/geojson#ch.are.bauzonen
wmts:https://wmts10.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml#ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill
```
*Note:* Support for WMTS in Data Url is currently only implemented when using `qwc-docker`.

*Note:* You can pass parameters which control the behaviour of the WMS client in QGIS Server by prefexing the parameters with `extwms.` when the layer is requested by QGIS Server, i.e. when printing. Example to override the step width/heigth of the QGIS WMS Client:
```text
wms:http://wms.geo.admin.ch?extwms.stepWidth=4096&extwms.stepHeight=4096#ch.swisstopo.pixelkarte-farbe-pk1000.noscale
```
**Manually configuring external layers**

Rather than setting the "Data Url", you can provide a manual `ExternalLayerDefinition` as follows:

| Entry                                                  | Description                                                                       |
|--------------------------------------------------------|-----------------------------------------------------------------------------------|
| `{`                                                    |                                                                                   |
| `⁣  "name": "<external_layer_name>",`                   | The name of the external layer, as referenced in the theme definitions.           |
| `⁣  "type": "<layer_type>",`                            | Layer type, "wms" or "wmts"                                                       |
| `⁣  "url": "<wms_baseurl>",       `                     | The WMS URL or WMTS resource URL for the external layer.                          |
| `}`                                                    |                                                                                   |

For external WMS layers, the following additional parameters apply:

| Entry                                                  | Description                                                                       |
|--------------------------------------------------------|-----------------------------------------------------------------------------------|
| `"params": {`                                          | Parameters for the GetMap request.                                                |
| `⁣  "LAYERS": "<wms_layername>,..."`,             | Comma-separated list of WMS layer names.                                          |
| `⁣  "OPACITIES": "<0-255>,..."`                   | Optional, if WMS server supports opacities.                                       |
| `},`                                                   |                                                                                   |
| `"featureInfoUrl": "<wms_featureinfo_baseurl>",`       | Optional, base URL for WMS GetFeatureInfo, if different from `url`.               |
| `"legendUrl": "<wms_legendgraphic_baseurl>"   ,`       | Optional, base URL for WMS GetLegendGraphic, if different from `url`.             |
| `"queryLayers": ["<wms_featureinfo_layername>", ...],` | Optional, list of GetFeatureInfo query layers, if different from `params.LAYERS`. |
| `"infoFormats": ["<featureinfo_format>", ...]`         | List of GetFeatureInfo query formats which the WMS service supports.              |

For external WMTS layers, the following additional parameters apply (you can use the [`qwc2/scripts/wmts_config_generator.py`](https://github.com/qgis/qwc2/blob/master/scripts/wmts_config_generator.py) script to obtain these values):

| Entry                                                  | Description                                                                       |
|--------------------------------------------------------|-----------------------------------------------------------------------------------|
| `"tileMatrixSet": "<tile_matrix_set_name>",`           | The name of the tile matrix set.                                                  |
| `"originX": <origin_x>,`                               | The X origin of the tile matrix.                                                  |
| `"originY": <origin_y>,`                               | The Y origin of the tile matrix.                                                  |
| `"projection": "EPSG:<code>",`                         | The layer projection.                                                             |
| `"resolutions": [<resolution>, ...],`                  | The list of WMTS resolutions.                                                     |
| `"tileSize": [<tile_width>, <tile_height>]`            | The tile width and height.                                                        |

### Theme info links <a name="theme-info-links"></a>

You can specify links to display in an info-menu next to the respective theme title in the theme switcher entries.

The format of a `ThemeInfoLinkDefinition` is as follows:

| Entry                       | Description                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------|
| `"name": "<link_name>",`    | The name of the link, as referenced in the theme definitions.                     |
| `"title": "<link_title>",`  | The title for the link, as displayed in the info menu of the theme entry in the theme switcher. |
| `"url": "<link>",`          | A link URL.                                                                       |
| `"target": "<link_target>"` | The link target, i.e. `_blank`.                                                   |

*Note*: When using `qwc-services`, theme info links must be explicitly permitted by creating appropriate `Theme info link` resources and permissions in the `qwc-admin-gui`.

### Plugin data <a name="plugin-data"></a>

Plugin data is useful to provide a per-theme configuration for custom plugins. The format for a `PluginDataReource` is as follows:


| Entry                       | Description                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------|
| `"name": "<resource_name>",`| The name of the resource.                                                         |
| `"...": ...,`               | Arbitrary additional fields.                                                      |

*Note*: When using `qwc-services`, theme plugin data entries must be explicitly permitted by creating appropriate `Plugin data` resources (as child of a respective `Plugin` resource) and permissions in the `qwc-admin-gui`.

### Background layers <a name="background-layers"></a>

Background layers are handled completely client-side and do not appear in the layer tree.

The format of the background layer definitions is as follows:

| Entry                            | Description                                                                       |
|----------------------------------|-----------------------------------------------------------------------------------|
| `"name": "<Name>",`              | The name of the background layer, used in the theme definitions.                  |
| `"title": "<Title>",`            | The title of the background layer, as displayed in the background switcher.       |
| `"titleMsgId": "<Title msgID>",` | Alternative to `title`, a message ID, translated through the translation files.   |
| `"thumbnail": "<Filename>",`     | Optional, image file in `assets/img/mapthumbs` (see [Viewer assets](ViewerConfiguration.md#viewer-asset)). Defaults to `img/mapthumbs/default.jpg`.        |
| `"type": "<Type>",`              | The background layer type, i.e. `wms` or `wmts`.                                  |
| `"attribution": "<Attribution>",`| Optional, attribution which will be shown in the bottom right corner of the map.  |
| `"attributionUrl": "<URL>",`     | Optional, link associated to the attribution                                      |
| `"group": "<GroupId>",`          | Optional, a group ID string. Background layers with the same group ID will be grouped together in the background switcher. |
| `"minScale": <min_scale>,`       | Optional, minimum scale denominator from which to render the layer.               |
| `"maxScale": <max_scale>,`       | Optional, maximum scale denominator from which to render the layer.               |
| `"layerConfig": {...},`          | Optional, extra OpenLayers layer configuration, according to the [API](https://openlayers.org/en/latest/apidoc) of the specific layer type. |
| `"sourceConfig": {...},`         | Optional, extra OpenLayers source configuration, according to the [API](https://openlayers.org/en/latest/apidoc) of the specific source type. |
| `<Layer params>`                 | Parameters according to the specified layer type.                                 |

Some minimal examples of supported background layers:

* *WMS*:
```json
{
  "name": "swissboundaries",
  "type":"wms",
  "url":"https://wms.geo.admin.ch",
  "params": {
    "LAYERS": "ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill",
    "VERSION": "1.3.0",
    ...
  }
}
```

* *WMTS*:
```json
{
  "name":"bluemarble",
  "type":"wmts",
  "url":"http://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_ShadedRelief/default/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.jpeg",
  "bbox":{
    "bounds":[-180.0,-85.051129,180.0,85.051129],
    "crs":"EPSG:4326"
  },
  "originX":-20037508.34278925,
  "originY":20037508.34278925,
  "projection:":"EPSG:3857",
  "resolutions":[156543.03390625,78271.516953125,39135.7584765625,19567.87923828125,9783.939619140625,4891.9698095703125,2445.9849047851562,1222.9924523925781],
  "tileMatrixPrefix":"",
  "tileMatrixSet":"GoogleMapsCompatible_Level8",
  "tileSize":[256,256]
}
```
*Note*: You can use the helper python script located at `qwc2/scripts/wmts_config_generator.py` to easily generate WMTS background layer configurations.

* *OpenStreetMap*:
```json
  {
    "name":"mapnik",
    "type":"osm"
  }
```

* *Bing*:
```json
  {
    "name": "bing",
    "type": "bing",
    "apiKey": "<get from https://www.bingmapsportal.com/>",
    "imagerySet": "<Aerial|AerialWithLabelsOnDemand|RoadOnDemand|CanvasDark|OrdnanceSurvey>"
  }
```

* *XYZ*:
```json
  {
    "name": "OpenCycleMap",
    "type": "xyz",
    "url":"https://{a-c}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png"
  }
```

* *VectorTiles*: (note: if the tile projection is not `EPSG:3857`, you need to specifiy `projection` and `tileGridConfig`)
```json
  {
    "name": "mvt_example",
    "type": "mvt",
    "url": "http://foobar.baz/tileset/{z}/{x}/{y}.pbf",
    "style": "http://foobar.baz/style.json",
    "projection": "EPSG:XXXX",
    "tileGridConfig": {
      "origin": [<x>, <y>],
      "resolutions": [<resolutions>]
    }
  }
```

Alternatively, WMS and WMTS background layers can also be defined specifiying a resource identifier, which will then be resolved at runtime. For example:
```json
{
    "name":"ch.swisstopo.pixelkarte-grau",
    "title":"National map (gray)",
    "resource": "wmts:https://wmts10.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml#ch.swisstopo.pixelkarte-grau",
    "thumbnail":"img/mapthumbs/default.jpg"
}
```
A background layer definition can also be a group of layers, in the format
```json
{
  "name": "<Name>",
  "title": "<Title>",
  "type": "group",
  "items": [
    { <BackgroundLayerDefinition> },
    { <BackgroundLayerDefinition> },
    ...
  ]
}
```
Instead of specifiying a full background layer definition in a group, you can also reference an existing one with `"ref": "<bg_layer_name>"`, and selectively override certain properties, such as `minScale` and `maxScale`:
```json
{
  ...
  "items": [
    {
      "ref": "<bg_layer_name>",
      "minScale": <min_scale>,
      "maxScale": <max_scale>
    },
    ...
  ]
}
```

## Generating the themes configuration <a name="generating-theme-configuration"></a>

The file ultimately read by the QWC2 viewer is the `themes.json` configuration, which includes the contents of `themesConfig.json` completed with additional data obtained from the QGIS Project.

* When using `qwc-docker`, you can generate the themes from the `qwc-admin-gui` administration backend, running on <http://localhost:8088/qwc_admin> by default. Log in as `admin` user, then press the green `Generate service configuration` button. This will invoce the`qwc-config-generator`, which will generate `mapViewerConfig.json` located below `qwc-docker/volumes/config/<tentant>`. You can then inspect the generated `themes.json` at <http://localhost:8088/themes.json>.

* When using QWC2 as a standalone viewer, the `themes.json` can be generated by invoking
```bash
yarn run themesconfig
```
  Note: this command is automatically invoked when starting the development server via `yarn start`.

  If working in an environment without node, using the equivalent command
```bash
python3 qwc2/scripts/themesConfig.py
```
  If you want to manage multiple `themesConfig.json` files, you can specify which while should be processed by the theme generation script via the `QWC2_THEMES_CONFIG` environment variable.

## Storing projects in database <a name="projects-in-database"></a>

When you are using `qwc-docker`, you can configure QWC to read the QGIS projects directly from the database. To do this, proceed as follows:

- Set up a PostgreSQL database connection in QGIS, checking the "Allow saving/loading QGIS projects in the database" option.
- Save the project to the configured database in QGIS using Project &rarr; Save To &rarr; PostgreSQL.
- Add a `qgisprojects` service definition for the used database to `qwc-docker/pg_service.conf`.
- Write a theme configuration entry in `themesConfig.json` using with `"url": "/ows/pg/<schema>/<projectname>"`, where `schema` and `projectname` as as specified when saving the project in QGIS.

## Split categorized layers

When using `qwc-docker`, the `qwc-config-generator` has the ability to split a layer that has been [classified](https://docs.qgis.org/latest/en/docs/training_manual/vector_classification/classification.html) with QGIS into multiple layers and move them into a new group (the group name will be the original layer name). To activate this functionality, follow these steps:

1. Place the projects whose layers you want to split below `qwc-docker/volumes/config-in/<tenant>/qgis_projects`.

2. In the topolevel `config` in `qwc-docker/volumes/config-in/<tenant>/tenantConfig.json`, ensure `qgis_projects_gen_base_dir` is set and valid, and set `"split_categorized_layers": true`.

3. For all layers that you want to split, create the [variable](https://docs.qgis.org/latest/en/docs/user_manual/working_with_vector/vector_properties.html#variables-properties) `convert_categorized_layer` and set it to `true`.

4. Generate the [themes configuration](#generating-theme-configuration). The `qwc-config-generator` will process the projects and write the modified projects to `qgis_projects_gen_base_dir`.

*Note:* Make sure you are using `qwc-config-generator:v<version>` and not `qwc-config-generator:v<version>-noqgis`.
