# Map export

The [MapExport](../references/qwc2_plugins.md#mapexport) plugin allows exporting a selected portion of the map to a variety of formats, as supported by the QGIS Server, among which:

* Image formats (`image/png`, `image/jpeg`, `image/geotiff`, ...)
* DXF (`application/dxf`)
* GeoPDF (`application/pdf`)

See the [MapExport plugin reference](../references/qwc2_plugins.md#mapexport) for a list of configuration options.

In particular, the plugin supports specifying different export configurations for each format, i.e.:
```
      {
        "name": "MapExport",
        "cfg": {
          "formatConfiguration": {
            "application/dxf": [
              {"name": "default"},
              {
                "name": "Geobau",
                "extraQuery": "LAYERS=dxfgeobau",
                "formatOptions": "MODE:NOSYMBOLOGY"
              }
            ],
            "image/png": [
              {"name": "default"},
              {"name": "With baselayer", "baseLayer": "SWISSIMAGE"}
            ]
          }
        }
      },
```

For each format, if multiple configurations are defined, a combobox will be displayed to choose an export configuration.

## Export to image formats
For image formats, it may be desired to override the background layer for the exported map. To this end, specify a `baseLayer` in the format configuration to the name of a background `printLayer`.

For GeoTIFF image export to become available, set up the `wms_geotiff_output` [QGIS Server plugin](https://github.com/qwc-services/qwc-qgis-server-plugins):

```yml
  qwc-qgis-server:
    image: docker.io/sourcepole/qwc-qgis-server:<TAG>
    volumes:
      - ./volumes/qgis-server-plugins/wms_geotiff_output:/usr/share/qgis/python/plugins/wms_geotiff_output:ro
    ...
```

# DXF export
To enable the DXF export format, the desired layers are marked as *Published* in the QGIS Project Properties &to; QGIS Server &to; WFS/OAPIF.

You can configure the DXF export by passing supported [`FORMAT_OPTIONS`](https://docs.qgis.org/latest/en/docs/server_manual/services.html#wms-formatoptions) as `formatOptions`, i.e.

    "formatOptions": "MODE:NOSYMBOLOGY;NO_MTEXT:1"

# GeoPDF export
GeoPDF export is available since QGIS Server 3.36. As opposed generating a PDF via `GetPrint` (as used by the `Print`-Plugin), the MapExport plugin generates the GeoPDF via `GetMap` and will return just the selected export area as a GeoPDF, without relying on any print layout defined in the QGIS project.

You can configure the GeoPDF export by passing supported `FORMAT_OPTIONS`, look for `PdfFormatOption` in [https://github.com/qgis/QGIS/blob/master/src/server/services/wms/qgswmsparameters.h](https://github.com/qgis/QGIS/blob/master/src/server/services/wms/qgswmsparameters.h).
