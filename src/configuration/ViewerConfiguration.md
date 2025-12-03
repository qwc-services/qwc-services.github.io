# QWC Viewer Configuration

This chapter describes how to customize the QWC viewer.

First of all, it is important to keep in mind that the QWC viewer is designed to be a modular and highly customizeable application. Configuration falls into three categories:

- [Load-time configuration](#load-time-config): configuration applied when the application is loaded.
- [Customizing the assets](#viewer-asset): specify additional search providers, customize the color schemes, etc...
- [Compiling a custom viewer](#custom-viewer): configure which components which are built into the application, add own plugins, etc...

The QWC stock application (and the `qwc-map-viewer` docker image) serve as a good starting point, and for simple viewers the load-time configuration options are often sufficient to avoid the need of building a customized application.

## Load-time configuration `config.json`<a name="load-time-config"></a>

The load-time configuration `config.json` configuration file contains global viewer settings as well as the viewer plugin configuration for mobile and desktop devices. It is located as follows:

- `qwc-docker`: `qwc-docker/volumes/config-in/<tentant>/config.json`
- Standalone viewer: `qwc-app/static/config.json`

Refer to the [sample `config.json`](https://github.com/qgis/qwc2/blob/master/static/config.json) for a concrete example.

### Global settings

All settings are optional, with fallback to the default values as documented.

| Setting                             | Description |
|-------------------------------------|-------------|
|`allowFractionalZoom`                | Whether to allow arbitrary scales for viewing the map. Default: `false`. |
|`assetsPath`                         | Relative path to the `assets` folder. Default: `"assets"`. |
|`bearingFormat`                      | Format of bearing measurement. Default value is `"bearing"` which shows angle in degrees, minutes and seconds with N/S prefix and W/E suffix, `"azimuth"` is shown as 0° to 360°, `"azimuth180"` is shown as -180° to +180°, `"bearingEW"` is shown as 0° to 180° with E/W suffix.|
|`bearingPrecision`                   | Defines number of decimals for bearing angle shown in degrees. Default: `0`. |
|`defaultColorScheme`                 | The color scheme to use. See [Color schemes](#color-schemes) for details. Default: `"default"`. |
|`defaultFeatureStyle`                | The default style to use for selection geometries and other unstyled features. Default: see [`qwc2/utils/FeatureStyles.js`](https://raw.githubusercontent.com/qgis/qwc2/refs/heads/master/utils/FeatureStyles.js). |
|`defaultInteractionStyle`            | The default style to use on geometries to measure, snap or edit. Default: see [`qwc2/utils/FeatureStyles.js`](https://raw.githubusercontent.com/qgis/qwc2/refs/heads/master/utils/FeatureStyles.js). |
|`defaultMarkerStyle`                 | The default style to use as marker icon. Default: see [`qwc2/utils/FeatureStyles.js`](https://raw.githubusercontent.com/qgis/qwc2/refs/heads/master/utils/FeatureStyles.js). |
|`editingAddLinkAnchors`              | Whether to automatically insert link anchors in text values when editing. Default: `true`, |
|`editServiceCaptchaSiteKey`          | ReCAPTCHA public site key for public editing, see [ReCAPTCHA validation](../topics/Editing.md#recaptcha). |
|`editTextNullValue`                  | A text value which represents `NULL` when editing. Default: `""`. |
|`geodesicMeasurements`               | Whether to perform measurements on the geoid. Default: `false`. |
|`loadTranslationOverrides`           | Whether to attempt to load tanslation overrides, see [Translations](../topics/Translations.md). Default: `false`. |
|`localeAwareNumbers`                 | Whether to use locale aware numbers throughout. Default: `false`. |
|`measurementPrecision`               | Number of decimal digits to display in measurements. Default: `2`. |
|`omitUrlParameterUpdates`            | Whether to omit updating the URL parameters. Default: `false`. |
|`projections`                        | A list of map projections to register, in the format `{"code": "<code>", "proj": "<proj4def>", "label": "<label>", "precision": <decimals>}`. By default, `EPSG:3857` and `EPSG:4326` are registered. |
|`qgisServerVersion`                  | The QGIS Server major version in use. Default: `3`. |
|`startupTask`                        | Task to automatically activate on application start, in the format `{key: "<Task>", "mode": "<Mode>"}`. |
|`storeAllLayersInPermalink`          | Whether to store the full layertree in the permalink data, rather than only local (i.e. redlining) layers. If `false`, remote layers are re-queried from the respective services, if `true`, they are statically reloaded (meaning restored layers may be outdated compared to current service capabilities). Default: `false`. |
|`tilePreloadLevels`                  | For tiled layers, load low-resolution tiles up to preload levels. 0 means no preloading. Default: `0`. |
|`translationsPath`                   | Relative path to the `translations` folder. Default: `"translations"`.   |
|`trustWmsCapabilityURLs`             | Whether to trust the GetMap etc. URLs reported in WMS service capabilities. If not `true`, the protocol, host and pathname portion of the URLs are inherited from the called capabilities URL. Default: `false`. |
|`urlPositionCrs`                     | The CRS used to encode the current map extent coordinates in the URL. Default: the current map projection. |
|`urlPositionFormat`                  | How to encode the current map extent in the URL, either `"centerAndZoom"` or `"extent"`. See [URL parameters](../topics/Interfacing.md#url-parameters) for details. Default: `"extent"`. |
|`urlRegEx`                           | A [JSON-escaped](https://www.freeformatter.com/json-escape.html) regular expression used to match URLs in feature attribute values. Default: see [`qwc2/utils/MiscUtils.js`](https://raw.githubusercontent.com/qgis/qwc2/refs/heads/master/utils/MiscUtils.js). |
|`wmsHidpi`                           | Whether to honour the device pixel ratio for WMS GetMap requests. Default: `true`. |
|`wmsMaxGetUrlLength`                 | URL length limit before switching to a POST request for GetMap and GetFeatureInfo. Default: `2048`. |
|`wmsWktPrecision`                    | Precision (as number of decimals) of WKT geometries passed in WMS requests. Default: `4`. |

### Global settings, overridable per theme<a name="theme-overridable-settings"></a>

The following options can be specified globally, and also overriden per theme, see [`themesConfig.json`](ThemesConfiguration.md).
All settings are optional, with fallback to the default values as documented.

| Setting                              | Description |
|--------------------------------------|-------------|
|`allowAddingOtherThemes`              | Whether to allow adding another theme to a currently loaded theme. Default: `false`. |
|`allowLayerTreeSeparators`            | Allows users to add separator items in a flat layer tree. Default: `false`.   |
|`allowRemovingThemeLayers`            | Whether to allow removing any theme layers from the layer tree. Default: `false`. |
|`allowReorderingLayers`               | Whether to allow re-ordering layers in the layer tree. Default: `false`.      |
|`disableImportingLocalLayers`         | Whether to hide the option to import local layers from the layer tree. Default: `false`. |
|`flattenLayerTreeGroups`              | Whether to display a flat layer tree, omitting the groups. Default: `false`.  |
|`globallyDisableDetachableDialogs`    | Whether to globally disable the detachable feature of popup dialogs. Default: `false`. |
|`globallyDisableDockableDialogs`      | Whether to globally disable the dockable feature of popup dialogs. Default: `false`. |
|`globallyDisableMaximizeableDialogs`  | Whether to globally disable the maximizeable feature of popup dialogs. Default: `false`. |
|`identifyTool`                        | The name of the identify plugin to use as default identify tool. If set to an empty string, no identify tool will be active by default. Default: `"Identify"`. |
|`importLayerUrlPresets`               | A list of predefined URLs from which the user can choose when importing layers from the layer tree. Entries must be strings or objects of the format `{"label": "<Label>", "value": "<URL>"}`. |
|`preserveBackgroundOnThemeSwitch`     | Whether to preserve the current background layer when switching theme, if possible. Default: `false`. |
|`preserveExtentOnThemeSwitch`         | Whether to preserve the current map extent when switching theme, if possible (see below). Default: `false`. |
|`preserveNonThemeLayersOnThemeSwitch` | Whether to preserve non-theme layers when switching theme. Default: `false`.  |
|`preventSplittingGroupsWhenReordering`| Whether to prevent splitting sibling groups or the group itself when reordering items. Default: `false`. |
|`searchFilterRegions`                 | List of predefined search filter regions, see [Search filtering](../topics/Search.md#filtering). |
|`searchThemeLayers`                   | Whether to allow searching for theme layers from the global search field. Default: `false`. |
|`searchThemes`                        | Whether to allow searching for themes from the global search field. Default: `false`. |
|`startupTask`                         | Task to automatically start when switching to the theme, in the format `{key: "<Task>", "mode": "<Mode>"}`. Takes precedence over the global `startupTask`. Note that the task is activated whenever switching to the theme, not only on application start. |

Note:

- The layer tree supports re-ordering layers via drag-and-drop if `allowReorderingLayers = true` *and either* `preventSplittingGroupsWhenReordering = true` *or* `flattenLayerTreeGroups = true`.
- If `preserveExtentOnThemeSwitch = true`, the current extent is preserved if it is within the new theme extent and if the current theme map projection is equal to the new theme projection. If `preserveExtentOnThemeSwitch = "force"`, the current extent is preserved regardless of whether it is within the new theme extent, but the current and new theme map projections must still match.

### Separate `mobile` / `desktop` global settings

You can specify the global settings separately for `mobile` and `desktop` by setting these in a corresponding toplevel section, i.e.:

```json
{
  "<prop>": "<value>", // This property applies for both mobile and desktop
   ...
  "mobile": {
    "<prop>: "<value>", // This property applies only for mobile
    ...
  },
  "desktop": {
    "<prop>: "<value>", // This property applies only for desktop
    ...
  }
}
```

You can also specify separate `mobile` and `desktop` sections in the `config` block of a theme item.

### URLs of external services

Some plugins require external services (typically part of the `qwc-services` ecosystem). When using the `qwc-docker`, these configuration entries will be automatically injected into the `config.json` for enabled services.

| Setting              | Description |
|----------------------|-------------|
|`authServiceUrl`      | Typically the URL of a QWC authentication service like `qwc-db-auth`. |
|`editServiceUrl`      | Typically the URL of the `qwc-data-service`.             |
|`elevationServiceUrl` | Typically the URL of the `qwc-elevation-service`.        |
|`documentService`     | Typically the URL of the `qwc-document-service`.         |
|`mapInfoService`      | Typically the URL of the `qwc-map-info-service`.         |
|`permalinkServiceUrl` | Typically the URL of the `qwc-permalink-service`.        |
|`searchServiceUrl`    | Typically the URL of the `qwc-fulltext-search-service`.  |

### Plugin configuration<a name="plugin-configuration"></a>

The plugin configuration is entered as follows:
```json
"plugins": {
  "common": [{<PluginConfig>}, ...],
  "mobile": [{<PluginConfig>}, ...],
  "desktop": [{<PluginConfig>}, ...]
}
```
The final `mobile` and `desktop` configurations will be computed by merging the `common` configuration with the respective specific configuration. Each `<PluginConfig>` block is of the format

| Setting                                         | Description                                                                         |
|-------------------------------------------------|-------------------------------------------------------------------------------------|
|`{`                                              |                                                                                     |
|`⁣  "name": "<name>",`                            | The plugin name.                                                                    |
|`⁣  "cfg": {...},`                                | The plugin configuration options, see [plugin reference](../references/qwc2_plugins.md). |
|`⁣  "mapClickAction": <"identify"|"unset"|null>,` | Optional: in case the plugin activates a viewer task, determines whether a click in the map will result in the identify tool being invoked, the task being unset, or whether no particular action should be performed (default). |
|`}`                                              |                                                                                     |

Any plugin configuration option can be overridden per theme in the theme item `config` section as follows:

```json
{
  "plugins": {
    "<plugin_name>": {
      "<cfg_prop>": <value>,
      ...
    },
    ...
  },
  "mobile": {
    "plugins: {...}, // Plugin config props applied only for mobile
    ...
  },
  "desktop": {
    "plugins: {...}, // Plugin config props applied only for desktop
    ...
  }
}
```

In general, the procedure for enabling a plugin is:

* Make sure the plugin is compiled into the application (see [Build-time configuration](#build-time configuration)).
* In the `plugins` section of `config.json`, below `common` (or `mobile` and/or `desktop`), add an entry
    ```json
    {
        "name": "<Plugin name>",
        "cfg": {
          <Plugin configuration props>
        },
        "order": <render_order>
    }
    ```
    where `order` is optional and denotes the render order, useful to control the tab-focus order. Default is `0`, can be an arbitrary positive or negative number.
* For most plugins (i.e. those which launch as an explicit task in the viewer), add entries in `menuItems` and/or `toolbarItems` in the `TopBar` configuration. The format of these entires is as follows:

| Setting                                    | Description                                                                       |
|--------------------------------------------|-----------------------------------------------------------------------------------|
|`{`                                         |                                                                                   |
|`⁣  "key": "<key>",`                         | The name of a plugin, i.e. `LayerTree`. The label for the entry will be looked up from the translations using the `appmenu.items.<key>` message identifier (see [Translations](../topics/Translations.md). |
|`⁣  "icon": "<icon>",`                       | The icon of the entry, either a built-in icon name (see below), or `:/<path_to_asset>` containing the path relative to `assetsPath` of an asset image. |
|`⁣  "themeBlacklist": ["<themename>", ...],` | Optional, allows specifying a blacklist of theme names or titles for which the entry should not be visible. |
|`⁣  "themeWhitelist": ["<themename>", ...],` | Optional, allows specifying a whitelist of theme names or titles for which the entry should be visible. |
|`⁣  "themeFlagBlacklist": ["<flag1>", ...],` | Optional, allows specifying a blacklist of [theme flags](ThemesConfiguration.md#manual-theme-configuration) for which the entry should not be visible. |
|`⁣  "themeFlagWhitelist": ["<flag1>", ...],` | Optional, allows specifying a whitelist of [theme flags](ThemesConfiguration.md#manual-theme-configuration) for which the entry should be visible. |
|`⁣  "mode": "<mode>",`                       | Optional, depending on the plugin, a mode can be configured to launch the plugin directly in a specific mode. For instance, the `Measure` plugin supports specifying the measurement mode (`Point`, `LineString`, `Polygon`). |
|`⁣  "requireAuth": "<true|false>",`          | Optional, the entry is only visible when user is logged-in.                       |
|`⁣  "shortcut": "<shortcut>"`                | Optional, keyboard shortcut which triggers the entry, i.e. `"alt+shift+a"`.       |
|`}`                                         |                                                                                   |

  *Note:* The built-in icons are those located in [`qwc2/icons`](https://github.com/qgis/qwc2/tree/master/icons) and in `qwc-app/icons`. The built-in icon names are the respective file names, without `.svg` extension.


**Opening external websites**<a name="opening-external-websites"></a>

As a special case, entries for opening external URLs can be defined in the `menuItems` and/or `toolbarItems` in the `TopBar` configuration as follows:

| Setting                | Description                                                                       |
|------------------------|-----------------------------------------------------------------------------------|
|`{`                     |                                                                                   |
|`⁣  "key": "<key>",`     | An arbitrary key (not used by existing plugins), used to lookup the label for the entry from the translations (as `appmenu.items.<key>`). |
|`⁣  "title": "<key>",`   | Optional: Title to use insead of `appmenu.items.<key>`.                           |
|`⁣  "icon": "<icon>",`   | As above.                                                                         |
|`⁣  "url": "<url>",`     | The URL to open. Can contain as placeholders the keys listed in [URL Parameters](../topics/Interfacing.md#url-parameters), enclosed in `$` (i.e. `$e$` for the extent). In addition, the placeholders `$x$` and `$y$` for the individual map center coordinates as well as `$lang$` for the viewer language are also supported.               |
|`⁣  "target": "<target>"`| The target where to open the URL, if empty, `_blank` is assumed. Can be `iframe` or `:iframedialog:<windowname>:<options>` (see below) to open the link in a iframe window inside QWC. |
|`}`                     |                                                                                   |

The format of the `:iframedialog:<windowname>:<options>` target is as follows:

- `windowname` is used to identify the name of the iframe window within which the link will be opened, i.e. can be used to make multiple external URLs re-use the same iframe window.
- `options` is a sequence of `<key>=<value>`, separated by `:`, with the following options:

    - `dockable=<false|left|right|top|bottom>`: whether the window is dockable, and to which screen edge
    - `docked=<true|false>`: whether the window is docked by default
    - `splitScreenWhenDocked=<true|false>`: whether to split the screen when docked
    - `h=<h>`: the initial window height
    - `w=<w>`: the initial window width
    - `zIndex=<zIndex>`: the stacking zIndex for the dialog
    - `icon=<icon>`: the name of a build-in icon (see [`qwc2/icons`](https://github.com/qgis/qwc2/tree/master/icons)) to display in the window title bar (overrides the icon set in the `menuItems`/`tollbarItems` entry)
    - `title=<title>`: the title to display in the window title bar (overrides the title set in the `menuItems`/`tollbarItems` entry)
    - `print=<true|false>`: whether to display a print icon in the window title bar


## Customizing the viewer assets <a name="viewer-assets"></a>

The viewer assets are located as follows:

- Standalone viewer: `qwc-app/static/assets`
- `qwc-docker`: `qwc-docker/volumes/qwc2/assets`

The default structure of the assets folder is as follows:

| Path                      | Description
|---------------------------|---------------------------------------------------------------------------|
|`└─ assets/`               | See [Viewer assets](#viewer-assets)                                       |
|`   ├─ css/`               | Additional style sheets, must be included by `index.html`.                |
|`   │  ├─ colorschemes.css`| Additional color schemes.                                                 |
|`   │  └─ qwc2.css`        | Additional style definitions.                                             |
|`   ├─ img/`               | Application logo etc.                                                     |
|`   │  ├─ genmapthumbs/`   | Autogenerated map thumbnails.                                             |
|`   │  └─ mapthumbs/`      | Map thumbnails.                                                           |
|`   ├─ templates/`         |                                                                           |
|`   │  └─ legendprint.html`| HTML template for the legend print.                                       |
|`   ├─ help.html`          | Help dialog fragment, see [Help dialog](#help-dialog).                    |
|`   └─ searchProviders.js` | Additional search providers, see [Search providers](../topics/Search.md). |

Furthermore, the application entry point `index.html` is located as follows:

- Standalone viewer: `qwc-app/index.html`
- `qwc-docker`: `qwc-docker/volumes/config-in/<tenant>/index.html`

This file noteably specifies the application title, and references many of the assets located below the `assets` folder.

### Customizing the color scheme
The QWC color scheme is fully customizeable via CSS. A default color-scheme is built-in (see [DefaultColorScheme.css](https://github.com/qgis/qwc2/blob/master/components/style/DefaultColorScheme.css)). To define a custom color scheme, copy the default color scheme to `assets/css/colorschemes.css`, add an appropriate class name to the `:root` selector, and modify the colors as desided. Two additional examples (`highcontrast` and `dark`) are provided by default in[`assets/css/colorschemes.css`](https://github.com/qgis/qwc2/blob/master/static/assets/css/colorschemes.css).

You can then modify the color scheme which is applied by default by setting `defaultColorScheme` in `config.json` to an appropriate class name (i.e. `highcontrast` or `dark`).

To change the color scheme at runtime in QWC, make sure the `Settings` plugin is enabled, and in the `Settings` plugin configuration block in `config.json` list the color schemes below `colorSchemes`. Refer to the [sample `config.json`](https://github.com/qgis/qwc2/blob/master/static/config.json).

*Note*: When changing the color scheme via Settings dialog in QWC, the picked color scheme is stored in the browser local storage, and this setting will override the `defaultColorScheme` setting from `config.json`. Specifying the `style` URL-parameter (see [URL parameters](../topics/Interfacing.md#url-parameters)) will take precedence over all other settings.

*Note:* Make sure that `assets/css/colorschemes.css` is included in `index.html`.

### Overriding component styles

Occasionally, it may be desired to customize the styling on the QWC components. The recommended approach is to add the corresponding style overrides to `assets/css/qwc2.css`.

*Note:* Make sure that `assets/css/qwc2.css` is included in `index.html`.

### Customizing the application logo

The application logo in its various shapes and sizes are located below `assets/img/`. In particular, the `logo.svg` and `logo-mobile.svg` images are displayed as in the top left corner of QWC in desktop and mobile mode respectively. If you'd like to use another format than SVG (while keeping `logo` and `logo-mobile` as base name), you can change `logoFormat` in the `TopBar` configuration block in `config.json`.

### Providing custom map thumbnails

By default, when generating the themes configuration (see [theme configuration](ThemesConfiguration.md#generating-theme-configuration)), a default map thumbnail is generating via WMS `GetMap`, and placed below `assets/img/genmapthumbs`. You can provide your own thumbnail images instead by placing the corresponding images below `assets/img/mapthumbs` and referencing these as `thumbnail` in you theme configuration block in [`themesConig.json`](ThemesConfiguration.md#writing-themes-configuration).

### Personalizing the help dialog <a name="help-dialog"></a>

You can personalize the help dialog by providing a plain HTML document fragment in `static/assets/help.html` and configuring the `Help` plugin accordingly in `config.json`:
```json
{
  "name": "Help",
  "cfg": {
    "bodyContentsFragmentUrl": "assets/help.html"
  }
}
```
*Note:* `$VERSION$` can be used in the HTML document fragment as a placeholder for the application build date.

### Personalizing the legend print template

The legend print template `assets/templates/legendprint.html` is used when printing the map legend from the layer tree. The only requirement for this template is that is must contain a `<div id="legendcontainer"></div>` element.

## Building a custom viewer <a name="custom-viewer"></a>

The QWC stock application, hosted at [https://github.com/qgis/qwc2/](https://github.com/qgis/qwc2/), can serve as a base for building a custom application, and is published as an [NPM package](https://www.npmjs.com/package/qwc2). The LTS branch is published on NPM as [qwc2-lts](https://www.npmjs.com/package/qwc2-lts). An example of a custom application is hosted at [https://github.com/qgis/qwc2-demo-app](https://github.com/qgis/qwc2-demo-app).

To build a custom viewer, the first step is cloning the demo application:
```bash
git clone https://github.com/qgis/qwc2-demo-app.git qwc-app
```
The typical layout of a QWC app source tree is as follows:

| Path                         | Description
|------------------------------|-----------------------------------------------------------------------|
|`├─ static/`                  |                                                                       |
|`│  ├─ assets/`               | See [Viewer assets](#viewer-assets)                                   |
|`│  ├─ translations/`         | Translation files.                                                    |
|`│  ├─ config.json`           | Runtime configuration file.                                           |
|`   ├─ themesConfig.json`     | Themes configuration, edited manually.                                |
|`│  └─ themes.json`           | Generated theme configuration, autogenerated from `themesConfig.json`.|
|`├─ js/`                      |                                                                       |
|`│  ├─ app.jsx`               | Entry point of the ReactJS application.                               |
|`│  ├─ appConfig.js`          | Build-time configuration file.                                        |
|`│  ├─ Help.jsx`              | Built-in component of custom Help dialog, see [Help dialog](#help-dialog). |
|`│  └─ SearchProviders.js`    | Built-in custom search providers, see [Search providers](#search-providers). |
|`├─ icons/`                   | Application icons.                                                    |
|`├─ index.html`               | Entry point.                                                          |
|`├─ package.json`             | NodeJS configuration file.                                            |
|`└─ webpack.config.js`        | Webpack configuration.                                                |

### Application build-time configuration<a name="build-time configuration"></a>

The `js/appConfig.js` is the the principal build-time configuation file, and defines:

- The default application locale, built into the application. This locale is used if no available locale matches the browser locale.
- Which plugins are built into the application. Plugins left out here will be completely omitted when compiling the application bundle, and will hence also reduce the size of the bundle.
- Various hook functions, as documented in the sample [sample `js/appConfig.js`](https://github.com/qgis/qwc2-demo-app/blob/master/js/appConfig.js).

Refer to the [sample `appConfig.js`](https://github.com/qgis/qwc2-demo-app/blob/master/js/appConfig.js) for a concrete example.

### Overriding icons

The common application icons are located in `qwc2/icons`. They can be overridden by creating an icon with the same filename in the application specific `icons` folder.

*Note*: The icons in the `icons` folder are compiled into an icon font. The icons need to be black content on transparent background, and all drawings (including texts) must be converted to paths for the icons to render correctly.

### Compiling an application bundle

After tweaking the source files as desired, compile a deployable application bundle for production running
```bash
yarn run prod
```
When using `qwc-docker`, copy the contents of the `qwc-app/prod` folder to `qwc-docker/volumes/qwc2` and edit the `qwc-docker/docker-compose.yml` to use `qwc-map-viewer-base` with your custom build:
```yml
qwc-map-viewer:
  image: sourcepole/qwc-map-viewer-base:vYYYY.MM.DD
  environment:
    <<: *qwc-service-variables
    SERVICE_MOUNTPOINT: '/'
  volumes:
    - ./pg_service.conf:/srv/pg_service.conf:ro
    - ./volumes/config:/srv/qwc_service/config:ro
    - ./volumes/qwc2:/qwc2:ro
```
### Keeping the QWC application up to date

To update the base QWC components, just update the version of the `qwc2` dependency in `package.json`.

The [QWC Upgrade Notes](../release_notes/QWC2UpgradeNotes.md) documents major changes, and in particular all incompatible changes between releases which require changes to the application specific code and/or configuration.
