# Interfacing with other applications

QWC offers a number of options to interface it with other applications.

## URL parameters <a name="url-parameters"></a>

The following parameters can appear in the URL of the QWC application:

- `t`: The active theme
- `l`: The layers in the map, see below.
- `bl`: The visible background layer
- `e`: The visible extent
- `c`: The center of the visible extent
- `s`: The current scale
- `crs`: The CRS of extent/center coordinates
- `hc`: If `c` is specified and `hc` is `true` or `1`, a marker is set at `c` when starting the application. Note: requires the `StartupMarkerPlugin` plugin to be active.
- `ic`: If `c` is specified and `ic` is `true` or `1`, a marker is set at `c` when starting the application.
- `st`: The search text
- `hp`, `hf`: Startup highlight parameters used in conjunction with the `qwc-fulltext-search-service`, see below.
- `f`: A filter configuration, see [Map filtering](./MapFilter.md).
- `localConfig`: Override the name of the loaded config file, i.e. to load `myconfig.json` instead of the default `config.json`, pass `localConfig=myconfig`.
- `v`: Which view to load: `2d` for the 2D view, `3d` for the fullscreen 3D view, `3d2d` for the split-screen 3D/2D view.
- `v3d`: The 3D view, as `camera_x,camera_y,camera_z,target_x,target_y,target_z,h`, where `camera` is the camera position, `target` the scene target ("look at") position. If `h` is specified and non-zero, a first-person-view is assumed and `h` denotes the height above terrain of the camera.
- `bl3d`: The visible background layer in the 3D view.

The `l` parameter lists all layers in the map (redlining and background layers) as a comma separated list of entries of the form
```text
<layername>[<transparency>]{<style>}!
```
where
- `layername` is the WMS name of a theme layer or group, or an external layer resource string in the format
```text
<wms|wfs>:<service_url>#<layername>
```
   for external layers, i.e. `wms:https://wms.geo.admin.ch/?#ch.are.bauzonen`.
- `<transparency>` denotes the layer transparency, betwen 0 and 100. If the `[<transparency>]` portion is omitted, the layer is fully opaque.
- `<style>` denotes the layer style name. If the `{<style>}` portion is omitted, the style named `default` will be used, if one exists, or the first available style otherwise.
- `!` denotes that the layer is invisible (i.e. unchecked in the layer tree). If omitted, the layer is visible.

*Note*: If group name is specified instead of the layer name, QWC will automatically resolve this to all layer names contained in that group, and will apply transparency and visibility settings as specified for the group.

The `urlPositionFormat` parameter in `config.json` determines whether the extent or the center and scale appears in the URL.

The `urlPositionCrs` parameter in `config.json` determines the projection to use for the extent resp. center coordinates in the URL. By default the map projection of the current theme is used. If `urlPositionCrs` is equal to the map projection, the `crs` parameter is omitted in the URL.

### Highlight feature on startup

If a search text passed via `st` results in a unique result, the viewer automatically zooms to this result on startup. If the search result does not provide a bounding box, the `minScale` defined in the `searchOptions` of the `TopBar` configuration in `config.json` is used.

When using the `qwc-fulltext-search-service`, you can hightlight a feature on startup as follows:
- Either specify `hp=<facet_name>&hf=<filter_expr>`
- Or specify `st=<filter_expr>&hp=<facet_name>`

See [Fulltext search](Search.md#fulltext-search) for more details.

## Launching external websites

QWC menu entries can be configured to launch external websites as described in [opening external websites](../configuration/ViewerConfiguration.md#opening-external-websites).

## Javascript API

The `API` plugin exposes many application actions via the `window.qwc2` object and makes them accessible for external applications. See [API plugin reference](../references/qwc2_plugins.md#api) for more details.

See [api_examples.js](https://github.com/qgis/qwc2-demo-app/blob/master/static/api_examples.js) for some concrete examples.

