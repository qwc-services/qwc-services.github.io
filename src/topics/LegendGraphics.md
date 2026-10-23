# Legend graphics

By default, QWC will obtain the legend graphics of a layer from QGIS Server.

## Customizing the `GetLegendGraphics` request
You can customize the `GetLegendGraphics` request by specifying additional query parameters in via `extraLegendParameters` in the [theme configuration block](../configuration/ThemesConfiguration.md#manual-theme-configuration). The list of supported query parameters is documented in the [QGIS Server documentation](https://docs.qgis.org/latest/en/docs/server_manual/services/wms.html#wms-getlegendgraphics).

## Providing custom legend images
The `qwc-ogc-service` supports service custom legend images.

The OGC service supports custom layer legend images, which will be matched in this order (the first one found is used):

- As base64, as set in `<layer_resource_config>[legend_image_base64]`
- A filename as set in `<layer_resource_config>[legend_image]`
- A filename matching `<legend_images_path>/<service_name>/<layername>_<style>_<suffix>.png`
- A filename matching `<legend_images_path>/<service_name>/<layername>_<suffix>.png`
- A filename matching `<legend_images_path>/<service_name>/default_<suffix>.png`
- A filename matching `<legend_images_path>/<service_name>/<layername>_<style>.png`
- A filename matching `<legend_images_path>/<service_name>/<layername>.png`
- A filename matching `<legend_images_path>/<resource_entry[legend_image]>`
- A filename matching `<legend_images_path>/<service_name>/default.png`

Where

* `legend_images_path` is the directory containing custom legend images, configured in the service configuration.
* `service_name` is the name of the WMS service
* `layername` is the WMS layer name
* `suffix`: empty, or one of `_thumbnail`, `_tooltip`. The suffix is passed by QWC to the legend service depending on the requested image type
* `resource_entry[legend_image]` and `resource_entry[legend_image_base64]` are the `legend_image` resp. `legend_image_base64` settings of a layer as configured in the service resource configuration, for example:
```json
{
  "name": "ogc",
  "config": ...,
  "resources": {
    "wms_services": [
      {
        "name": "<service name>",
        "root_layer": {
          "name": "<root_layer_name>",
          "layers": [
            {
              "name": "<layer_name>",
              "legend_image": "/path/to/legend_image.png"
            }
          ]
        }
      }
    ]
  }
}
```

*Note*: When running `qwc-ogc-service` in Docker, mount the legend templates folder into the `qwc-ogc-service` container, i.e.:
```yml
  qwc-ogc-service:
    image: sourcepole/qwc-ogc-service:vYYYY.MM.DD
    volumes:
      ...
      - ./volumes/legends:/legends
```
and set `legend_images_path` to `/legends` in the service configuration.
