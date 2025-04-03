# Legend graphics

By default, QWC will obtain the legend graphics of a layer from QGIS Server.

## Customizing the `GetLegendGraphics` request
You can customize the `GetLegendGraphics` request by specifying additional query parameters in via `extraLegendParameters` in the [theme configuration block](../configuration/ThemesConfiguration.md#manual-theme-configuration). The list of supported query parameters is documented in the [QGIS Server documentation](https://docs.qgis.org/latest/en/docs/server_manual/services/wms.html#wms-getlegendgraphics).

## Providing custom legend images
You can provide custom legend images by [enabling](../configuration/ServiceConfiguration.md#enabling-services) the `qwc-legend-service`.

Mount the legend folder into the `qwc-legend-service` container, i.e.:
```yml
  qwc-legend-service:
    image: sourcepole/qwc-feature-info-service:vYYYY.MM.DD
    volumes:
      ...
      - ./volumes/legends:/legends
```

*Note:* If mounting to another location than `/legends`, set the `legend_images_path` in the `legend` service configuration in `tenantConfig.json`:
```json
{
  "name": "legend",
  "config": {
    "legend_images_path": "/<path>/"
  }
}
```

Then, legend images will be searched for in this order (the first one found is used):

 * A `<legend_images_path>/<service_name>/<layername><suffix>.png` file, where
    * `service_name` is the name of the WMS service
    * `layername` is the WMS layer name
    * `suffix`: empty, or one of `_thumbnail`, `_tooltip`. The suffix is passed by QWC to the legend service depending on the requested image type.
 * A `<legend_images_path>/<legend_image>` file with `legend_image` as specified for the desired layer in the `legend` service configuration, for example:
```json
{
  "name": "legend",
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
              "legend_image": "edit_points.png"
            }
          ]
        }
      }
    ]
  }
}
```
 * A `<legend_images_path>/default<suffix>.png` file for a default legend image, with `suffix` as documented above.
