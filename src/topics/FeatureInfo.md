# Feature info

The feature info behaviour in QWC is controlled by configuring `identifyTool` in `config.json` (or per-theme in `themesConfig.json`) to the desired plugin as well as whether a `qwc-feature-info-service` is used.

The feature info is by default triggered when clicking on a feature in the map. You can also configure the feature info as an explicit viewer tool by setting `identifyTool: null` and [adding](../configuration/ViewerConfiguration.md#plugin-configuration) a `menuItems` or `toolbarItems` entry.

The following approaches are available for feature info:

- `Identify` plugin:
 - [WMS GetFeatureInfo](#wms-getfeatureinfo), rendered in a table or in a custom HTML template
 - [DB feature info](#db-feature-info) with custom SQL queries
- [`FeatureForm` plugin](#feature-form): custom attribute forms with `qwc-data-service`

## WMS GetFeatureInfo<a name="wms-getfeatureinfo"></a>

To query features over WMS GetFeatureInfo, set `identifyTool: "Identify"`. By default, results are displayed in a table. To display the results in a custom HTML template, the `qwc-feature-info-service` [can be used](../configuration/ServiceConfiguration.md#enabling-services).

*Note:* Use of the `qwc-feature-info-service` is also recommended if the `qwc-data-service` is used for editing, to ensure attribute values containing paths to uploaded files are properly converted to clickable hyperlinks.

Set whether a layer is identifyable in `QGIS → Project Properties → Data sources`.

To highlight the geometry, make sure `QGIS → Project Properties → QGIS Server → Add geometry to feature response` is checked.

### Suppressing attributes

You can suppress attributes globally by selecting "Do not expose via WMS" in QGIS → Layer properties → Fields.

Alternatively, you can selectively restrict attributes using the `qwc-admin-gui` and assigning `Attribute` resource permissions as desired.

You can also omit empty attributes by setting `skipEmptyFeatureAttributes: true` in the theme configuration entry in `themesConfig.json`.

If you use the `qwc-feature-info-service`, you can also omit empty attributes directly in the `GetFeatureInfo` by setting `skip_empty_attributes: true` in the `featureInfo` service configuration in `tenantConfig.json`.

### Attribute values: HTML markup, hyperlinks, images

In general, HTML markup in attribute values is preserved.

For displaying interactive hyperlinks, the following options are supported:

- URLs in attribute text values with no HTML markup are automatically converted to an interactive hyperlink.
- Alternatively, you can enclose the URL in a HTML `<a>` tag in the attribute value. To open the linked page in an inline dialog within QWC, you can set the anchor target to `:iframedialog:<dialogname>:<optkey>=<optval>:<optkey>=<optval>:...` where the supported options are:
  * `w`: Dialog width in pixels, default: `640`.
  * `h`: Dialog height in pixels, default: `480`.
  * `title`: Dialog window title, by default the translation string `windows.<dialogname>`.
  * `print`: Whether to add a print icon for printing the dialog contents, default: `true`.
  * `dockable`: Whether the dialog can be docked, default `false`.
  * `docked`: Whether the dialog is initially docked, default `false`.
  Example:
```
<a href="https://example.com" target=":iframedialog:w=1024:h=768:title=Example">Link text</a>
```
For displaying images, the following options are supported:

- If `replaceImageUrls: true` is set in the `Identify` plugin configuration in `config.json`, attribute text values which contain exactly an URL to an image are converted to inline images. If you use the `qwc-feature-info-service`, you need to set `transform_image_urls` in the `featureInfo` service configuration in `tenantConfig.json`.
- Alternatively, you can add a `<img>` tag directly in the attribute value.

This applies in particular to `<a />` anchor and `<img />` tags for displaying links an images in an attribute value.

### Client side attribute transformations

This functionality is only available *without* the `qwc-feature-info-service`.

To compute derived attributes client-side, you can implement the `customAttributeCalculator` in `qwc2-app/js/IdentifyExtensions.js` (which is passed to the `Identify` plugin in `appConfig.js`).

To transform attributes client-side you can implement the `attributeTransform` in `qwc2-app/js/IdentifyExtensions.js` (which is passed to the `Identify` plugin in `appConfig.js`).

### Custom export

By default, the identify dialog in QWC allows you to export the results to `json` (QWC feature storage format), `geojson` (standard GeoJSON without QWC specific fields), `csv` (single CSV with all layers) or `csv+zip` (ZIP with one CSV per layer). You can define additional export functions by extending `customExporters` in `qwc2-app/js/IdentifyExtensions.js`.

### Custom HTML templates<a name="html-templates"></a>

You can specify a custom HTML template for displaying the feature rather than the default table view by [enabling](../configuration/ServiceConfiguration.md#enabling-services) the `qwc-feature-info-service`.

Mount the info templates folder into the `qwc-feature-info-service` container, i.e.:
```yml
  qwc-feature-info-service:
    image: sourcepole/qwc-feature-info-service:vYYYY.MM.DD
    volumes:
      ...
      - ./volumes/info_templates:/info_templates
```

*Note:* If mounting to another location than `/info_templates`, set the `info_templates_path` in the `featureInfo` service configuration in `tenantConfig.json`:
```json
{
  "name": "featureInfo",
  "config": {
    "info_templates_path": "/<path>/"
  }
}
```

Then, info templates will be searched by name as `<info_templates_path>/<service_name>/<layername>.html`.

Alternatively, you can specify the template in the `featureInfo` service configuration in `tenantConfig.json`, either inline or as a path:
```json
{
  "name": "featureInfo",
  "config": ...,
  "resources": {
    "wms_services": [
      {
        "name": "<service_name>",
        "root_layer": {
          "name": "<root_layer_name>",
          "layers": [
            {
              "name": "<layer_name>",
              "info_template": {
                <See below>
              }
            }
          ]
        }
      }
    ]
  }
}
```
Example `info_template` with inline template:
```json
"info_template": {
  "type": "wms",
  "template": "<div><h2>Demo Template</h2>Pos: {{ x }}, {{ y }}<br>Name: {{ feature.Name }}</div>"
}
```

Example `info_template` with template path:
```json
"info_template": {
  "type": "wms",
  "template_path": "/info_templates/template.html"
}
```

*Note:*

- `x` and `y` are the info query coordinates. `feature.<attr>` renders the `attr` attribute value of the feature.
- The templates must be HTML fragments *without* `html` or `body` tags.
- The templates folder needs to be mounted into the `qwc-feature-info-service` container, i.e.:
```yml
  qwc-feature-info-service:
    image: sourcepole/qwc-feature-info-service:vYYYY.MM.DD
    volumes:
      ...
      - ./volumes/info-templates:/info_templates:ro
```

## DB query feature info<a name="db-feature-info"></a>

When using the `Identify` plugin and the `qwc-feature-info-service`, you can query features directly from a database instead of over WMS GetFeatureInfo, by providing the `featureInfo` service configuration as described in [HTML templates](#html-templates), but specifying a `db_url` and `sql`, for example
```json
"info_template": {
  "type": "sql",
  "db_url": "postgresql:///?service=qwc_geodb",
  "sql": "SELECT ogc_fid as _fid_, name, formal_en, pop_est, subregion, ST_AsText(wkb_geometry) as wkt_geom FROM qwc_geodb.ne_10m_admin_0_countries WHERE ST_Intersects(wkb_geometry, ST_GeomFromText(:geom, :srid)) LIMIT :feature_count;",
  "template": "<div><h2>Demo Template</h2>Pos: {{ x }}, {{ y }}<br>Name: {{ feature.Name }}</div>"
}
```
*Note:* `x`, `y` and `geom` are passed as parameters to the SQL query. If a `GetFeatureInfo` request is being processed with a `filter_geom` parameter, `geom` will correspond to that parameter. Otherwise `geom` will be `POINT(x y)`.

## Localization

The `qwc-feature-info-service` supports switching the runtime locale by setting the `LOCALE` environment variable, i.e.:
```yml
  qwc-feature-info-service:
    image: docker.io/sourcepole/qwc-feature-info-service:vXXXX.XX.XX
    environment:
      <<: *qwc-service-variables
      SERVICE_MOUNTPOINT: '/api/v1/featureinfo'
      LOCALE: 'de_DE'
```

In addition, the [`locale`](https://docs.python.org/3/library/locale.html) object is available in templates. This is particularly helpful for rendering locale-formatted numbers, i.e.

```html
<div>Area: {{ locale.format_string("%.2f", area, True) }}</div>
```

## Feature form<a name="feature-form"></a>

The `FeatureForm` plugin displays picked features in a feature form as configured in `QGIS → Layer properties → Attributes form`. It queries the features via `qwc-data-service`, and hence only works for layers with `postgresql` data source.

See [Designing the edit forms](Editing.md#edit-forms) for more information on designing edit forms.

To use it as default identify-tool, set `identifyTool: "FeatureForm"` in `config.json`.

A layer is only identifyable with the `FeatureForm` plugin if corresponding `Data` resources and permissions are configured for the layer data source in the `qwc-admin-gui`. If a write permission is configured, the feature will be editable.

## Permissions

When using the `Identify` plugin and the `qwc-feature-info-service`, you can manage the permissions in the `qwc-admin-gui` as follows:

* To restrict the display of single layer attributes to specific roles, create a `Layer` and `Attribute` resource (latter as child of the created `Layer` resource) and create permissions assigning the desired roles to the `Attribute` resources.
   * *Note*: The name of the `Attribute` resource needs to be equal to the attribute alias name if one is defined in the QGIS project!
* To restrict whether a layer is identifiable to specific roles, create a `FeatureInfo service` and `FeatureInfo layer` resource (latter as child of the created `FeatureInfo service` resource), and create permissions assigning the desired roles to the `FeatureInfo layer` resources.

When using the `FeatureForm` plugin and the `qwc-data-service`, the `Data` resource permissions are used, see [Editing](Editing.md#quick-start).
