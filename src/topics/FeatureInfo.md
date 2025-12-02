# Feature info

The feature info displays attributes for picked objects. 

The following options are available for displaying feature info:

- [`Identify` plugin](#identify): display attributes in a table or custom HTML templates, querying the features via:

    - [WMS GetFeatureInfo](#wms-getfeatureinfo)
    - [Custom SQL queries](#db-feature-info)

- [`FeatureForm` plugin](#feature-form): display attributes in QGIS attribute forms, querying the features via the `qwc-data-service`

You can configure the identify tool by setting `identifyTool` in `config.json` (or per-theme in `themesConfig.json`).

By default, it is triggered when clicking on a feature in the map. You can also configure the feature info as an explicit viewer tool by setting `identifyTool: null` and [adding](../configuration/ViewerConfiguration.md#plugin-configuration) a `menuItems` or `toolbarItems` entry.

## Identify plugin<a name="identify"></a>

The identify plugin allows displaying feature attributes queried over WMS GetFeatureInfo or, by using the `qwc-feature-info-service`, from a custom SQL query.

To use it as default identify-tool, set `identifyTool: "Identify"` in `config.json`.

By default, results are displayed in a table. You can also display the results using a custom HTML template by using the `qwc-feature-info-service`.

You can also omit empty attributes by setting `skipEmptyFeatureAttributes: true` in the theme configuration entry in `themesConfig.json`.

*Note:* Use of the `qwc-feature-info-service` is also recommended if the `qwc-data-service` is used for editing, to ensure attribute values containing paths to uploaded files are properly converted to clickable hyperlinks.

### Querying features via WMS GetFeatureInfo<a name="wms-getfeatureinfo"></a>

Set whether a layer is identifyable in `QGIS → Project Properties → Data sources`.

To highlight the geometry, make sure `QGIS → Project Properties → QGIS Server → Add geometry to feature response` is checked.

You can suppress attributes globally by selecting "Do not expose via WMS" in QGIS → Layer properties → Fields.

Alternatively, you can selectively restrict attributes using the `qwc-admin-gui` and assigning `Attribute` resource permissions as desired, see [Permissions](#permissions).

If you use the `qwc-feature-info-service`, you can filter empty attributes service-side by setting `skip_empty_attributes: true` in the `featureInfo` service configuration in `tenantConfig.json`.

## Querying features via custom SQL queries<a name="db-feature-info"></a>

With the `qwc-feature-info-service`, you can query features directly from a database instead of over WMS GetFeatureInfo, by providing the `featureInfo` service configuration as described in [HTML templates](#html-templates), but specifying a `db_url` and `sql`, for example
```json
"info_template": {
  "type": "sql",
  "db_url": "postgresql:///?service=qwc_geodb",
  "sql": "SELECT ogc_fid as _fid_, name, formal_en, pop_est, subregion, ST_AsText(wkb_geometry) as wkt_geom FROM qwc_geodb.ne_10m_admin_0_countries WHERE ST_Intersects(wkb_geometry, ST_GeomFromText(:geom, :srid)) LIMIT :feature_count;",
  "template": "<div><h2>Demo Template</h2>Pos: {{ x }}, {{ y }}<br>Name: {{ feature.Name }}</div>"
}
```

In a DB Query the following values are replaced in the SQL:

* `:x`: X coordinate of query
* `:y`: Y coordinate of query
* `:srid`: SRID of query coordinates
* `:resolution`: Resolution in map units per pixel
* `:FI_POINT_TOLERANCE`: Tolerance for picking points, in pixels (default=16)
* `:FI_LINE_TOLERANCE`: Tolerance for picking lines, in pixels (default=8)
* `:FI_POLYGON_TOLERANCE`: Tolerance for picking polygons, in pixels (default=4)
* `:i`: X ordinate of query point on map, in pixels
* `:j`: Y ordinate of query point on map, in pixels
* `:height`: Height of map output, in pixels
* `:width`: Width of map output, in pixels
* `:bbox`: 'Bounding box for map extent as minx,miny,maxx,maxy'
* `:crs`: 'CRS for map extent'
* `:feature_count`: Max feature count
* `:with_geometry`: Whether to return geometries in response (default=1)
* `:with_maptip`: Whether to return maptip in response (default=1)
* `:geom`: The `filter_geom` passed to the `GetFeatureInfo` request, if any, otherwise `POINT(x y)`

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
    * `detachable`: Whether the dialog can be detached, default `true`.

  Example:
```
<a href="https://example.com" target=":iframedialog:w=1024:h=768:title=Example">Link text</a>
```
For displaying images, the following options are supported:

- If `replaceImageUrls: true` is set in the `Identify` plugin configuration in `config.json`, attribute text values which contain exactly an URL to an image are converted to inline images. If you use the `qwc-feature-info-service`, you need to set `transform_image_urls` in the `featureInfo` service configuration in `tenantConfig.json`.
- Alternatively, you can add a `<img>` tag directly in the attribute value.

This applies in particular to `<a />` anchor and `<img />` tags for displaying links an images in an attribute value.

### Client side attributes

To compute derived attributes client-side, you can register an attribute calculator via `window.qwc2.addIdentifyAttributeCalculator`, exposed by the [API](../references/qwc2_plugins.md#API) plugin.

### Custom export

By default, the identify dialog in QWC allows you to export the results to `json` (QWC feature storage format), `geojson` (standard GeoJSON without QWC specific fields), `csv` (single CSV with all layers) or `csv+zip` (ZIP with one CSV per layer). You can define additional export functions registering an exporter via `window.qwc2.addIdentifyExporter`, exposed by the [API](../references/qwc2_plugins.md#API) plugin.

### Custom HTML templates<a name="html-templates"></a>

With the `qwc-feature-info-service`, you can specify a custom HTML template for displaying the feature rather than the default table view.

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

The template must only contain the body content (without `head`, `script`, `body`).

This template can contain attribute value placeholders, in the form

    {{ feature.attr }}

which are replaced with the respective values when the template is rendered (using [Jinja2](http://jinja.pocoo.org/)).
The following values are available in the template:

* `x`, `y`, `crs`: Coordinates and CRS of info query
* `feature`: Feature with attributes from info result as properties, e.g. `feature.name`
* `fid`: Feature ID (if present)
* `bbox`: Feature bounding box as `[<minx>, <miny>, <maxx>, <maxy>]` (if present)
* `geometry`: Feature geometry as WKT (if present)
* `layer`: Layer name

To automatically detect hyperlinks in values and replace them as HTML links as well as transform image URLs to inline images the following helper can be used in the template:

    render_value(value)

When using [localized themes](./Translations.md#translated-themes), if you want to make QWC translate the attribute names, enclose these in `translate()`.

Example:

```xml
    <div>Result at coordinates {{ x }}, {{ y }}</div>
    <table>
        <tr>
            <td>translate(Name):</td>
            <td>{{ feature.name }}</td>
        </tr>
        <tr>
            <td>translate(Description):</td>
            <td>{{ feature.description }}</td>
        </tr>
        <tr>
            <td>translate(Link):</td>
            <td>{{ render_value(feature.link) }}</td>
        </tr>
    </table>
```


### Localization

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

### Permissions<a name="identify-permissions"></a>

If `permissions_default_allow` is set to `true` in `tenantConfig.json`, layers and attributes are queryable by default.

* To restrict the display of single layer attributes to specific roles, create a `Layer` and `Attribute` resource (latter as child of the created `Layer` resource) and create permissions assigning the desired roles to the `Attribute` resources.
* To restrict whether a layer can be queried, create a `FeatureInfo service` and `FeatureInfo layer` resource (latter as child of the created `FeatureInfo service` resource), and create permissions assigning the desired roles to the `FeatureInfo layer` resources.

## Feature form plugin<a name="feature-form"></a>

The `FeatureForm` plugin displays picked features in a feature form as configured in `QGIS → Layer properties → Attributes form`. It queries the features via `qwc-data-service`, and hence only works for layers with `postgresql` data source.

See [Designing the edit forms](Editing.md#edit-forms) for more information on designing edit forms.

To use it as default identify-tool, set `identifyTool: "FeatureForm"` in `config.json`.

A layer is only identifyable with the `FeatureForm` plugin if corresponding `Data` resources and permissions are configured for the layer data source in the `qwc-admin-gui`. If a write permission is configured, the feature will be editable.

### Permissions<a name="feature-form-permissions"></a>

The `FeatureForm` plugin relies on the `qwc-data-service` and the `Data` resource permissions, see [Editing](Editing.md#quick-start).
