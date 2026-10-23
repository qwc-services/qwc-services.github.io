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

The identify plugin allows displaying feature attributes queried over WMS GetFeatureInfo, if using the `qwc-ogc-service`, from a custom SQL query or a custom source.

To use it as default identify-tool, set `identifyTool: "Identify"` in `config.json`.

By default, results are displayed in a table. You can also display the results using a custom HTML template by using the `qwc-ogc-service`.

You can also omit empty attributes by setting `skipEmptyFeatureAttributes: true` in the theme configuration entry in `themesConfig.json`.

*Note:* If using the `qwc-data-service`, make sure the the `ogc` service configuration block contains  is used for editing, to ensure attribute values containing paths to uploaded files are properly converted to clickable hyperlinks.

### Querying features via WMS GetFeatureInfo<a name="wms-getfeatureinfo"></a>

Set whether a layer is identifyable in `QGIS → Project Properties → Data sources`.

To highlight the geometry, make sure `QGIS → Project Properties → QGIS Server → Add geometry to feature response` is checked.

You can suppress attributes globally by selecting "Do not expose via WMS" in QGIS → Layer properties → Fields.

Alternatively, you can selectively restrict attributes using the `qwc-admin-gui` and assigning `Attribute` resource permissions as desired, see [Permissions](#permissions).

If you use the `qwc-ogc-service`, you can filter empty attributes service-side by setting `skip_empty_attributes: true` in the `featureInfo` service configuration in `tenantConfig.json`.

### Display field <a name="displayfield"></a>

The display field configured in QGIS Vector Layer Properties &rarr; Display is used as display title of an identify result. If no display field ist configured, the fallback fields `name` and ` id` will be tried (case-insensitive). You can configure the fallback field names by setting `fallbackDisplayFields` to the list of desired fallback field names at top-level in `config.json`. If you set `fallbackDisplayFields` to an empty list, no fallback display name will be set.

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

- If `replaceImageUrls: true` is set in the `Identify` plugin configuration in `config.json`, attribute text values which contain exactly an URL to an image are converted to inline images. If you use the `qwc-ogc-service`, you need to set `transform_image_urls` in the `ogc` service configuration in `tenantConfig.json`.
- Alternatively, you can add a `<img>` tag directly in the attribute value.

This applies in particular to `<a />` anchor and `<img />` tags for displaying links an images in an attribute value.

### Client side attributes

To compute derived attributes client-side, you can register an attribute calculator via `window.qwc2.addIdentifyAttributeCalculator`, exposed by the [API](../references/qwc2_plugins.md#API) plugin.

### Exporting results

By default, the identify dialog in QWC allows you to export the results to `json` (QWC feature storage format), `geojson` (standard GeoJSON without QWC specific fields), `csv` (single CSV with all layers) or `csv+zip` (ZIP with one CSV per layer). You can define additional export functions registering an exporter via `window.qwc2.addIdentifyExporter`, exposed by the [API](../references/qwc2_plugins.md#API) plugin.

### Custom HTML templates

With the `qwc-ogc-service`, you can provide custom HTML templates for rendering the info results. These will be used for `text/html` as well as `text/xml` responses, in the latter case the FeatureInfo XML reponse will contain a `HtmlContent` element with the HTML output which QWC viewer will display.

A template can be specified as follows (in order of precedence):

- Via `template`, `template_base64` or `template_path` in the WMS layer resource configuration, i.e.
    ```json
    {
      "name": "edit_points",
      "attributes": [...],
      "info_template": {
        "template": "<Jinja2 template string>",
        "template_base64": "<base64 encoded Jinja2 template string>",
        "template_path": "<path to a html file containing a Jinja2 template>"
      }
    },
    ```
- Placing a `.html` file below `<info_templates_path>/<map_name>/<layer_name>.html`. This is usually the easier approach.


A template specified via resource configuration takes precedence over templates matched by filename below `info_templates_path`, as set in the service configuration.

*Note*: When running `qwc-ogc-service` in Docker, mount the info templates folder into the `qwc-ogc-service` container, i.e.:
```yml
  qwc-ogc-service:
    image: sourcepole/qwc-ogc-service:vYYYY.MM.DD
    volumes:
      ...
      - ./volumes/info_templates:/info_templates
```
and set `info_templates_path` to `/info_templates` in the service configuraiton. 

A template must only contain the body content (without `head`, `script`, `body`). The HTML can be styled using inline CSS, otherwise the CSS from the QWC viewer is used.

A template can contain attribute value placeholders, in the form `{{ feature.attr }}` which are replaced with the respective values when the template is rendered (using [Jinja2](http://jinja.pocoo.org/)).

The following values are available in the template:

* `x`, `y`, `crs`: Coordinates and CRS of info query
* `feature`: Feature with attributes from info result as properties, e.g. `feature.name`, as well as an `_attributes` array, see below.
* `fid`: Feature ID (if present)
* `bbox`: Feature bounding box as `[<minx>, <miny>, <maxx>, <maxy>]` (if present)
* `geometry`: Feature geometry as WKT (if present)
* `layer`: Layer name
* `render_value`: Function which detects special value formats and renders them accordingly
* `locale`: The [Locale module](https://docs.python.org/3/library/locale.html), allows i.e. locale aware number formatting
* `request`: The original request, useful for extracting i.e. request origin etc.

In particular:

- The `feature` object provides a list of its attributes:
    ```
    feature._attributes = [{
      'name': <attribute name>,
      'value': <attribute value>,
      'alias': <attribute alias>,
      'type': <attribute value data type as string>,
      'json_aliases': <JSON attribute aliases as {'json_key': 'value'}>
    }]
    ```
- The `render_value` function will transform:
  * Attribute values which match an image URL to an image if `transform_image_urls` is set to `true` in the service config.
  * Attribute values which match an URL to a clickable hyperlink, with the link text configurable via `info_link_text` in the service config.
  * Attribute values which match an email to a cllickable `mailto:` hyperlink.
  * Structured JSON attributes to subtables, as described below

- When the `qwc-ogc-service` Docker container, you can set the locale used by `locale` by setting the `LANG` environment variable. Since the `qwc-ogc-service` Docker image is based on Alpine and only contains minimal locale support, you may need to provide your own [locale convention](https://docs.python.org/3/library/locale.html?locale.localeconv) overrides, especially for number formatting, via the `LOCALECONV_OVERRIDES` environment variable. For example:
    ```yml
    environment:
      LANG: 'de_DE.UTF-8'
      LOCALECONV_OVERRIDES: '{"decimal_point": ",", "thousands_sep": "\'", "grouping": [3, 0]}'
    ```
    In a template, you can then use i.e. `{{ locale.format("%.3f", feature.number, grouping=True) }}`.

Example:

```xml
    <div>Result at coordinates {{ x }}, {{ y }}</div>
    <table>
        <tr>
            <td>Name:</td>
            <td>{{ feature.name }}</td>
        </tr>
        <tr>
            <td>Description:</td>
            <td>{{ feature.description }}</td>
        </tr>
        <tr>
            <td>Link:</td>
            <td>{{ render_value(feature.link) }}</td>
        </tr>
    </table>
```
When using [localized themes](./Translations.md#translated-themes), you can make the QWC viewer translate the attribute names by enclosing these in `translate()`, i.e. `translate(Description)`.

### SQL info queries<a name="db-feature-info"></a>

By default, WMS `GetFeatureInfo` are forwarded to the internal QGIS Server. You can instead query a DB via SQL.

Example configuration:
```json
"info_template": {
  "type": "sql",
  "db_url": "postgresql:///?service=qwc_geodb",
  "sql": "SELECT ogc_fid AS _fid_, name, formal_en, pop_est, subregion, ST_AsText(wkb_geometry) AS wkt_geom, Box2D(wkb_geometry) AS bbox FROM qwc_geodb.ne_10m_admin_0_countries WHERE ST_Intersects(wkb_geometry, ST_GeomFromText(:geom, :srid)) LIMIT :feature_count;"
}
```
In a DB query the following values are replaced in the SQL:

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

The query should return the feature ID as `_fid_`, the WKT geometry as `wkt_geom` and the BBOX as `bbox`. All other selected columns are used as feature attributes.

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
