# Printing

QWC2 supports printing to PDF via the QGIS Server `GetPrint` request.

The basic steps are:

* Ensure the `Print` plugin is enabled in the QWC2 viewer.
* Create print layouts in the QGIS project as desired. The layouts must contain one Map element.
* [Generate the themes configuration](../configuration/ThemesConfiguration.md#generating-theme-configuration).

The available print layouts will then appear in the QWC2 print plugin.

You can limit the available print scales by setting `printScales` (or `defaultPrintScales`) in the [theme configuration](../configuration/ThemesConfiguration.md#manual-theme-configuration) to a list of scale denominators. If the list is empty, the print scale can be freely chosen.

Similarly, you can limit the available print resolutions by setting `printResolutions` (or `defaultPrintResolutions`) in the theme configuration to a list of resolutions. If the list is empty, the print resolution can be freely chosen.

External WMS layers are automatically printed if the [Print plugin config option](../references/qwc2_plugins/#print) `printExternalLayers` is `true` (default). Note that printing external `WMTS` layers is currently not supported by the QGIS Server.

You can enable the option to generate a GeoPDF by setting the the Print plugin config option `allowGeoPdfExport` to `true`. *Note:* This is only supported on QGIS Server 3.32 and newer.

Some additional tasks include:

* [Configuring the print background layers](#background-layers)
* [Configuring user labels](#user-labels)
* [Configuring the print grid](#print-grid)
* [Configuring layouts with legend](#print-legend)
* [Configuring atlas printing](#print-atlas)

## Configuring print background layers <a name="background-layers"></a>

Background layers are handled purely client-side in QWC2. There are two options for printing the background layer:

The first option is to add a `printLayer` to the background layer entry when writing the [themes configuration](../configuration/ThemesConfiguration.md#manual-theme-configuration), i.e.:

```json
{
  ...
  "backgroundLayers": [
      {"name": "<background layer name>", "printLayer": "<qgis layer name or resource string>"}
  ]
}
```

You can set `printLayer` to a QGIS layer name, or to a resource string (i.e. `wms:<baseurl>#<layername>`). A QGIS layer marked as `printLayer` will be filtered out from the QWC2 layer tree, and hence will not be displayed in QWC2.

You can also set `printLayer` to a list `[{"maxScale": <scale>, "name": "<layer name>"}, ..., {"maxScale": null, "name": "<QGis layer name>"}]`, ordered in ascending order by `maxScale`. The last entry should have `maxScale` `null`, as the layer used for all remaining scales.

This approach allows i.e. using a WMTS background layer in the web client for higher performance, and using a WMS background layer when printing for higher quality/resolution.

The second option is to use WMS background layers, which are automatically printed as external layers.

## User labels <a name="user-labels"></a>

User labels appear as free-text input fields in the QWC2 print dialog. To configure user labels, it is sufficient to add item `id`s to layout label items in the print layout. The specified `id` will appear as input field label in the QWC2 print dialog.

*Note*: Label `id`s beginning with `__` (two underscore characters) are ignored as user labels by QWC2.

You can can customize the input field (max length, number of rows) by setting the `printLabelConfig` in the [theme configuration](../configuration/ThemesConfiguration.md#manual-theme-configuration).

Also, in the theme configuration, you can also set:

* `printLabelForSearchResult`: The `id` of the label to which to write the current search result label, if any.
* `printLabelForAttribution`: The `id` of the label to which to write the current map attribution text, if any.

If you set the [Print plugin config option](../references/qwc2_plugins/#print) `hideAutopopulatedFields` to `true`, these labels will not be shown in the print dialog, otherwise they will be displayed as read-only fields.

## Print grid <a name="print-grid"></a>

In alternative to configuring a grid directly in the print layout, one can also define a `printGrid` configuration in the [theme configuration](../configuration/ThemesConfiguration.md#manual-theme-configuration). For example

```json
"printGrid": {
  "s": 1000, "x": 500, "y": 500,
  "s": 2000, "y": 1000, "y": 1000,
  "s": 10000, "y": 5000, "y": 5000,
}
```

will print a `500x500` (map units) grid for scales up to `1:1000`, a `1000x1000` grid for scales up to `1:2000`, etc.

## Layouts with legend <a name="print-legend"></a>

The QWC2 print dialog will expose a toggle switch to enable the legend in the print output for layout `<layout_name>` if the QGIS project contains a second layout named `<layout_name>_legend`. The layout with the `_legend` suffix is expected to contain a legend item.

## Atlas printing <a name="print-atlas"></a>

To enable atlas printing in QWC2, configure the QGIS project as follows:

- Check the `Generate an atlas` checkbox in the desired layout in QGIS layout designer &rarr; Atlas &rarr; Atlas settings, selecting the coverage layer as desired.
- In the layout map item properties, check `Controlled by Atlas`.
- In the Project properties &rarr; QGIS Server, set `Maximum features for Atlas print requests` to the desired value.

QWC2 will then display a feature picked in the print dialog which will allow picking the desired atlas features, and QGIS Server will generate a multi-page PDF accordingly.

## Layout templates <a name="layout-templates"></a>

The [QGIS Server print templates plugin](https://github.com/qwc-services/qwc-qgis-server-plugins) allows providing a common set of print layouts to projects to avoid having to manage potentially identical print layouts multiple times in the individual projects.

To configure it in `qwc-docker`, proceed as follows:

* Download the [QGIS Server print templates plugin](https://github.com/qwc-services/qwc-qgis-server-plugins), i.e. to `volumes/qgis-server-plugins/print_templates`, choose a print layout folder (i.e. `volumes/print-layouts`) and configure the `qwc-qgis-server` container as follows:

```yml
  qwc-qgis-server:
    image: docker.io/sourcepole/qwc-qgis-server:<TAG>
    environment:
      FCGID_EXTRA_ENV: 'PRINT_LAYOUT_DIR'
      PRINT_LAYOUT_DIR: '/layouts'
    volumes:
      - ./volumes/qgis-server-plugins/print_templates:/usr/share/qgis/python/plugins/print_templates:ro
      - ./volumes/print-layouts:/layouts:ro
    ...
```

* Mount the print layout folder also into the config generator container:

```yml
qwc-config-service:
    image: docker.io/sourcepole/qwc-config-generator:<TAG>
    volumes:
      - ./volumes/print-layouts:/layouts:ro
      ...
```

* Extend the config generator configuration in `tenantConfig.json` by specifying the location of the print layouts dir:

```json
{
  "config": {
    "qgis_print_layouts_dir": "/layouts"
    ...
  }
  ...
}
```
