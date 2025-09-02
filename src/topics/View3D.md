# 3D View

QWC offers a full 3D view based on [THREE.js](https://threejs.org/) and [Giro3D](https://giro3d.org/). It allows displaying 3D objects, mainly served as 3D Tiles, on a terrain provided by a COG (Cloud Optimised GeoTIFF). Layers from the 2D view will be rendered as draped textures on the 3D terrain.

![QWC 3D Arch](../images/qwc3d.png?style=centerme)


## Configuring the 3D View

To enable the 3D view, you need to configure the plugin in `config.json`. A typical `View3D` plugin configuration may look as follows:
```json
{
  "name": "View3D",
  "cfg": {
    "pluginOptions": {
      "Identify3D": {
        "tileInfoServiceUrl": "/api/v1/tileinfo/objinfo?tileset={tileset}&objectid={objectid}"
      },
      "LayerTree3D": {
        "importedTilesBaseUrl": "/assets/"
      },
      "TopBar3D": {
        "menuItems": [
          {"key": "ThemeSwitcher", "icon": "themes"},
          {"key": "LayerTree3D", "icon": "layers"},
          {"key": "Draw3D", "icon": "draw"},
          {"key": "Measure3D", "icon": "measure"},
          {"key": "Compare3D", "icon": "compare"},
          {"key": "HideObjects3D", "icon": "eye"},
          {"key": "MapLight3D", "icon": "light"},
          {"key": "MapExport3D", "icon": "rasterexport"},
          {"key": "ExportObjects3D", "icon": "export"},
          {"key": "Share", "icon": "share"},
          {"key": "Bookmark", "icon": "bookmark"},
          {"key": "Help", "icon": "info"},
          {"key": "Settings3D", "icon": "cog"},
          {"key": "Settings", "icon": "cog"}
        ],
        "toolbarItems": [
          {"key": "Measure3D", "icon": "measure"}
        ]
      }
    }
  }
}
```
*NOTE*:

* The `menuItems` and `toolbarItems` can contain both 3D tools as well as generic tools (which are not specifically 2D map tools). If you run the 3D View in split-screen 3D+2D mode, only 3D tools will be displayed in the 3D window toolbar and menu. If you run the 3D View in fullscreen, all configured entries will be displayed. 
* Consult the [View3D plugin reference](../references/qwc2_plugins.md#view3d) as well as well as the [3D tool plugins reference](../references/qwc2_plugins.md#3d-plugins) for additional configuation options.

Next, to add a 3D View to a theme, add a `map3d` configuration to the desired theme item in [`themesConfig.json`](../configuration/ThemesConfiguration.md#manual-theme-configuration):
```
"map3d": {
    "initialView": {
      "camera": [x, y, z],
      "target": [x, y, z],
      "personHeight": h
    },
    "dtm": {"url": "<url_to_dtm.tif>", "crs": "<dtm_epsg_code>},
    "basemaps": [
         {"name": "<name_of_background_layer>", "visibility": true, "overview": true},
         {"name": "<name_of_background_layer>"},
         ...
    ],
    "tiles3d": [
         {
             "name": "<name>",
             "url": "<url_to_tileset.json>",
             "title": "<title>",
             "baseColor": "<css RGB(A) color string>",
             "idAttr": "<tile_feature_attr>",
             "styles": {"<styleName>", "<url_to_tilesetStyle.json>", ...},
             "style": "<styleName>",
             "colorAttr": "<tile_feature_attr>",
             "alphaAttr": "<tile_feature_attr>",
             "labelAttr": "<tile_feature_attr>",
         }
    ],
    "objects3d": [
        {
             "name": "<name>",
             "url": "<url_to_file.gltf>",
             "title": "<title>"
        }
    ]
}
```
Where:

- `initialView` is optional and allows to define the initial view when opening the 3D view. If `personHeight` is specified and greater than 0, the first-person view is activated. If not specified, the 2D view is synchronized.
- The `dtm` URL should point to a cloud optimized GeoTIFF.
- The background layer names refer to the names of the entries defined in `backgroundLayers` in the `themesConfig.json`. Additionally:

    - `visibility` controls the initially visibile background layer
    - `overview: true` controls the name of background layer to display in the overview map. If no background layer is marked with `overview: true`, the currently visibile background layer id dipslayed in the overview map.

- The `tiles3d` entry contains an optional list of 3d tiles to add to the scene, with:

    - `idAttr`: feature properties table attribute which stores the object id, used for styling and passed to `tileInfoServiceUrl` of the `Identify3D` plugin. Default: `id`.
    - `styles`: optional, available tileset styles. Takes precedente over `colorAttr`, `alphaAttr`, `labelAttr`.
    - `style`: optional, tileset style enabled by default.
    - `baseColor`: the fallback color for the tile objects, defaults to `white`.
    - `colorAttr`: optional, feature properties table attribute which stores the feature color, as a `0xRRGGBB` integer.
    - `alphaAttr`: optional, feature properties table attribute which stores the feature alpha (transparency), as an integer between `0` and `255`.
    - `labelAttr`: optional, feature properties table attribute which stores the feature label, displayed above the geometry.

- The `objects3d` entry contains an optional list of GLTF objects to add to the scene.

You can control whether a theme is loaded by default in 2D, 3D or splitscreen 2D/3D view via `startupView` in the [theme item configuration](../configuration/ThemesConfiguration.md#manual-theme-configuration).

*NOTE*: If a theme contains a `map3d` configuration, a view switcher map button will automatically be displayed.

### Permissions <a name="permissions"></a>

To restrict 3D tiles configured in `tiles3d` of a `map3d` theme configuration, create a `3D Tiles Tileset` resource named according to the `name` of the `tiles3d` entry and create permissions assigning the desired roles to the resources.

### Styling 3D tiles

The tileset style JSON is a [3D Tiles stylesheet](https://github.com/CesiumGS/3d-tiles/tree/main/specification/Styling),
of which currently the `color` section is supported, and which may in addition also contain a `featureStyles` section as follows:
```
{
    "color": {
       ...
    },
    "featureStyles": {
      "<object_id>": {
          "label": "<label>",
          "labelOffset": <offset>,
          "color": "<css RGB(A) color string>"
      }
   }
}
```
Where:

- `label` is an optional string with which to label the object.
- `labelOffset` is an optional number which represents the vertical offset between the object top and the label. Defaults to `80`.
- `color` is an optional CSS color string which defines the object color.

*Note*:

- The color declarations in the `featureStyles` section override any color resulting from a color expression in the `color` section.
- You must ensure that your 3D tiles properties table contains all attributes which are referenced as variables in a color expression!

### 3D Tile Info Service
The [qwc-3d-tile-info-service](../references/qwc-3d-tile-info-service_readme.md) serves two purposes:

- It provides additional info attributes for 3D Tiles via `/objinfo?tileset=<tileset_name>&objectid=<feature_id>`.
- It provides 3D Tiles stylesheets, converted from 2D `SLD` styles via `/tileinfo/stylesheet?tileset=<tileset_name>&stylename=<style_name>`.

To set up the `qwc-3d-tile-info-service`, add the following to `docker-compose.yml`:
```yml
  qwc-3d-tile-info-service:
    image: docker.io/sourcepole/qwc-3d-tile-info-service:<tag>
    environment:
      <<: *qwc-service-variables
      SERVICE_MOUNTPOINT: '/api/v1/tileinfo'
    volumes:
      - ./pg_service.conf:/srv/pg_service.conf:ro
      - ./volumes/config:/srv/qwc_service/config:ro
      - ./volumes/qgs-resources:/data:ro
```

and configure the route in the `api-gateway/nginx.conf`:
```
location /api/v1/tileinfo {
    proxy_pass http://qwc-3d-tile-info-service:9090;
}
```

Then, assuming a `buildings` 3D Tiles dataset configured as
```
"tiles3d":[
  {
    "name": "buildings",
    "url":" :/assets/3dtiles/buildings/tileset.json",
    "title":"Buildings",
    "idAttr":"gml_id",
    "styles":{"default":"/api/v1/tileinfo/stylesheet?tileset=buildings&stylename=default"},
    "style": "default"
  }
]
```
a possible `tileinfo` configuration in `tenantConfig.json` may look as follows:
```
{
      "name": "tileinfo",
      "config": {
        "info_datasets": {
          "buildings" : {
            "dataset": "/data/buildings2d.gpkg",
            "layername": "buildings2d",
            "idfield": "gml_id",
            "type": "gpkg",
            "attribute_aliases": {
              "function": "Building function",
              "description": "Description"
            },
            "attribute_blacklist": [
              "gml_id"
            ],
            "styles": {
              "default": {
                "filename": "/data/buildings.sld"
                // or
                "query": "SELECT styleSLD FROM layer_styles WHERE f_table_name = 'buildings'"
              }
            }
          }
        }
      }
    }
```
*NOTE*:

- The `idAttr` in the `tiles3d` entry of the themes configuration specifies the tile feature properties attribute which contains the feature id passed to `/objinfo`.
- The `idfield` in the `info_datasets` entry of the service configuration specifies the feature id attribute of the `buildings2d` dataset to use for looking up the feature id passed to `/objinfo`.


### Import

To import scene objects in formats other than GLTF, a `ogcProcessesUrl` in `config.json` needs to point to a BBOX OGC processes server.
