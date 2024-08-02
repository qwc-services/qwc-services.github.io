# QWC2 Viewer Configuration

This chapter describes how to customize the QWC2 viewer.

First of all, it is important to keep in mind that the QWC2 Viewer is designed to be a modular and highly customizeable application. Configuration falls into three categories:

- [Load-time configuration](#load-time-config): configuration applied when the application is loaded.
- [Customizing the assets](#viewer-asset): specify additional search providers, customize the color schemes, etc...
- [Compiling a custom viewer](#custom-viewer): configure which components which are built into the application, add own plugins, etc...

The `qwc2-demo-app` (and the `qwc-map-viewer-demo` docker image) serve as a good starting point, and for simple viewers the load-time configuration options are often sufficient to avoid the need of building a customized application.

## Load-time configuration `config.json`<a name="load-time-config"></a>

The load-time configuration `config.json` configuration file contains global viewer settings as well as the viewer plugin configuration for mobile and desktop devices. It is located as follows:

- `qwc-docker`: `qwc-docker/volumes/config-in/<tentant>/config.json`
- Standalone viewer: `qwc2-app/static/config.json`

Refer to the [sample `config.json`](https://github.com/qgis/qwc2-demo-app/blob/master/static/config.json) for a concrete example.

### Global settings

All settings are optional, with fallback to the default values as documented.

| Setting                             | Description |
|-------------------------------------|-------------|
|`assetsPath`                         | Relative path to the `assets` folder. Default value: `assets`.               |
|`translationsPath`                   | Relative path to the `translations` folder. Default value: `translations`.   |
|`loadTranslationOverrides`           | Whether to attempt to load tanslation overrides, see [translations](#translations). Default value: `false`. |
|`urlPositionFormat`                  | How to encode the current map extent in the URL, either `centerAndZoom` or `extent`. See [URL parameters](../topics/Interfacing.md#url-parameters) for details. Default value: `extent`. |
|`urlPositionCrs`                     | The CRS used to encode the current map extent coordinates in the URL. Default value: the map projection. |
|`omitUrlParameterUpdates`            | Whether to omit updating the URL parameters. Default value: `false`.      |
|`defaultFeatureStyle`                | The default style to use for selection geometries and other unstyled features. Default value: see `qwc2/utils/FeatureStyles.js`. |
|`defaultMarkerStyle`                 | The default style to use as marker icon. Default value: see `qwc2/utils/FeatureStyles.js`. |
|`defaultInteractionStyle`            | The default style to use on geometries to measure, snap or edit. Default value: see `qwc2/utils/FeatureStyles.js`. |
|`projections`                        | A list of map projections to register, in the format `{"code": "<code>", "proj": "<proj4def>", "label": "<label>"}`. By default, `EPSG:3857` and `EPSG:4326` are registered. |
|`allowFractionalZoom`                | Whether to allow arbitrary scales for viewing the map. Default value: `false`.      |
|`localeAwareNumbers`                 | Whether to use locale aware numbers throughout. Default value: `false`.             |
|`wmsHidpi`                           | Whether to honour the device pixel ratio for WMS GetMap requests. Default value: `true`. |
|`wmsMaxGetUrlLength`                 | URL length limit before switching to a POST request for GetMap and GetFeatureInfo. Default: 2048. |
|`wmsWktPrecision`                    | Precision (as number of decimals) of WKT geometries passed in WMS requests. Default: 4. |
|`qgisServerVersion`                  | The QGIS Server major version in use, defaults to `3`.|
|`defaultColorScheme`                 | The color scheme to use. See [Color schemes](#color-schemes) for details. |
|`startupTask`                        | Task to automatically activate on application start, in the format `{key: "<Task>", "mode": "<Mode>"}`. |
|`storeAllLayersInPermalink`          | Whether to store the full layertree in the permalink data, rather than only local (i.e. redlining) layers. If `false`, remote layers are re-queried from the respective services, if `true`, they are statically reloaded (meaning restored layers may be outdated compared to current service capabilities).
|`urlRegEx`                           | A [JSON-escaped](https://www.freeformatter.com/json-escape.html) regular expression used to match URLs in feature attribute values. Default: see `qwc2/utils/MiscUtils.js`. |
|`trustWmsCapabilityURLs`             | Whether to trust the GetMap etc. URLs reported in WMS service capabilities. If not `true`, the protocol, host and pathname portion of the URLs are inherited from the called capabilities URL. |
|`editServiceCaptchaSiteKey`          | ReCAPTCHA public site key for public editing, see [ReCAPTCHA validation](../Topics/Editing.md#recaptcha).
|`editTextNullValue`                  | A text value which represents `NULL` when editing.
|`editingAddLinkAnchors`              | Whether to automatically insert link anchors in text values when editing.

### Global settings, overridable per theme<a name="theme-overridable-settings"></a>

The following options can be specified globally, and also overriden per theme, see [`themesConfig.json`](ThemesConfiguration.md).
All settings are optional, with fallback to the default values as documented.

| Setting                              | Description |
|--------------------------------------|-------------|
|`preserveExtentOnThemeSwitch`         | Whether to preserve the current map extent when switching theme, if possible (see below). Default value: `false`. |
|`preserveBackgroundOnThemeSwitch`     | Whether to preserve the current background layer when switching theme, if possible. Default value: `false`. |
|`preserveNonThemeLayersOnThemeSwitch` | Whether to preserve non-theme layers when switching theme. Default value: `false`.  |
|`allowReorderingLayers`               | Whether to allow re-ordering layers in the layer tree. Default value: `false`.      |
|`flattenLayerTreeGroups`              | Whether to display a flat layer tree, omitting the groups. Default value: `false`.  |
|`allowLayerTreeSeparators`            | Allows users to add separator items in a flat layer tree. Default value: `false`.   |
|`preventSplittingGroupsWhenReordering`| Whether to prevent splitting sibling groups or the group itself when reordering items. Default value: `false`. |
|`allowRemovingThemeLayers`            | Whether to allow removing any theme layers from the layer tree. Default value: `false`. |
|`searchThemes`                        | Whether to allow searching for themes from the global search field. Default value: `false`. |
|`searchThemeLayers`                   | Whether to allow searching for theme layers from the global search field. Default value: `false`. |
|`allowAddingOtherThemes`              | Whether to allow adding another theme to a currently loaded theme. Default value: `false`. |
|`disableImportingLocalLayers`         | Whether to hide the option to import local layers from the layer tree. Default value: `false`. |
|`importLayerUrlPresets`               | A list of predefined URLs from which the user can choose when importing layers from the layer tree. Entries must be strings or objects of the format `{"label": "<Label>", "value": "<URL>"}`. |
|`identifyTool`                        | The name of the identify plugin to use as default identify tool. If set to an empty string, no identify tool will be active by default. Default value: `Identify`. |
|`globallyDisableDockableDialogs`      | Whether to globally disable the dockable feature of popup dialogs. Default value: `false`. |
|`globallyDisableMaximizeableDialogs`  | Whether to globally disable the maximizeable feature of popup dialogs. Default value: `false`. |
|`searchFilterRegions`                 | List of predefined search filter regions, see [Search filtering](../topics/Search.md#filtering). |
|`startupTask`                         | Task to automatically start when switching to the theme, in the format `{key: "<Task>", "mode": "<Mode>"}`. Takes precedence over the global `startupTask`. Note that the task whenever switching to the theme, not only on application start. |

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
|`mapInfoService`      | Typically the URL of the `qwc-map-info-service`.         |
|`permalinkServiceUrl` | Typically the URL of the `qwc-permalink-service`.        |
|`searchServiceUrl`    | Typically the URL of the `qwc-fulltext-search-service`.  |
|`featureReportService`| Typically the URL of the `qwc-document-service`.         |

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
A particularly interesting aspect is the configuration of the entries in the application menu and toolbar, i.e. the entries in `menuItems` and `toolbarItems` in the `TopBar` plugin configuration. The format of these entries is as follows:

| Setting                                    | Description                                                                       |
|--------------------------------------------|-----------------------------------------------------------------------------------|
|`{`                                         |                                                                                   |
|`⁣  "key": "<key>",`                         | The name of a plugin, i.e. `LayerTree`. The label for the entry will be looked up from the translations using the `appmenu.items.<key>` message identifier (see <a href="#translations">Managing translations</a>). |
|`⁣  "icon": "<icon>",`                       | The icon of the entry, either a built-in icon name (see below), or `:/<path_to_asset>` containing the path relative to `assetsPath` of an asset image. |
|`⁣  "themeBlacklist": ["<themename>", ...],` | Optional, allows specifying a blacklist of theme names or titles for which the entry should not be visible. |
|`⁣  "themeWhitelist": ["<themename>", ...],` | Optional, allows specifying a whitelist of theme names or titles for which the entry should be visible. |
|`⁣  "themeFlagBlacklist": ["<flag1>", ...],` | Optional, allows specifying a blacklist of [theme flags](ThemesConfiguration.md#manual-theme-configuration) for which the entry should not be visible. |
|`⁣  "themeFlagWhitelist": ["<flag1>", ...],` | Optional, allows specifying a whitelist of [theme flags](ThemesConfiguration.md#manual-theme-configuration) for which the entry should be visible. |
|`⁣  "mode": "<mode>",`                       | Optional, depending on the plugin, a mode can be configured to launch the plugin directly in a specific mode. For instance, the `Measure` plugin supports specifying the measurement mode (`Point`, `LineString`, `Polygon`). |
|`⁣  "requireAuth": "<true|false>",`          | Optional, the entry is only visible when user is logged-in.                       |
|`⁣  "shortcut": "<shortcut>"`                | Optional, keyboard shortcut which triggers the entry, i.e. `"alt+shift+a"`.       |
|`}`                                         |                                                                                   |

*Note:* The built-in icons are those located in [`qwc2-app/qwc2/icons`](https://github.com/qgis/qwc2/tree/master/icons) and in `qwc2-app/icons`. The built-in icon names are the respective file names, without `.svg` extension.

Also the map buttons ([LocationButton](../references/qwc2_plugins.md#locatebutton), [HomeButton](../references/qwc2_plugins.md#homebutton), [TaskButton](../references/qwc2_plugins.md#taskbutton), [ZoomButton](../references/qwc2_plugins.md#zoombutton)) support `themeFlagBlacklist` and `themeFlagWhitelist` for controlling the visibility based on the [theme flags](ThemesConfiguration.md#manual-theme-configuration).

**Opening external websites**<a name="opening-external-websites"></a>

As a special case, entries for opening external URLs can be defined as follows:

| Setting                | Description                                                                       |
|------------------------|-----------------------------------------------------------------------------------|
|`{`                     |                                                                                   |
|`⁣  "key": "<key>",`     | An arbitrary key (not used by existing plugins), used to lookup the label for the entry from the translations. |
|`⁣  "icon": "<icon>",`   | As above.                                                                         |
|`⁣  "url": "<url>",`     | The URL to open. Can contain as placeholders the keys listed in [URL Parameters](../topics/Interfacing.md#url-parameters), encolsed in `$` (i.e. `$e$` for the extent). In addition, the placeholders `$x$` and `$y$` for the individual map center coordinates are also supported. |
|`⁣  "target": "<target>"`| The target where to open the URL, if empty, `_blank` is assumed. Can be `iframe` to open the link in a iframe window inside QWC2. |
|`}`                     |                                                                                   |

In general, the procedure for enabling a plugin is:

* Make sure the plugin is compiled into the application (see [Build-time configuration](#build-time configuration)).
* In the `plugins` section of `config.json`, below `common` (or `mobile` and/or `desktop`), add an entry
```json
{
    "name": "<Plugin name>",
    "cfg": {
      <Plugin configuration props>
    }
}
```
* For most plugins (i.e. those which launch as an explicit task in the viewer), add entries in `menuItems` and/or `toolbarItems` as desired, i.e.
```json
  "menuItems": [
    ...
    {"key": "<Plugin name>", "icon": "<icon name>", ...}
  ]
```
## Customizing the viewer assets <a name="viewer-assets"></a>

The viewer assets are located as follows:

- Standalone viewer: `qwc2-app/static/assets`
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

- Standalone viewer: `qwc2-app/index.html`
- `qwc-docker`: `qwc-docker/volumes/config-in/<tenant>/index.html`

This file noteably specifies the application title, and references many of the assets located below the `assets` folder.

### Customizing the color scheme
The QWC2 color scheme is fully customizeable via CSS. A default color-scheme is built-in (see [DefaultColorScheme.css](https://github.com/qgis/qwc2/blob/master/components/style/DefaultColorScheme.css)). To define a custom color scheme, copy the default color scheme to `assets/css/colorschemes.css`, add an appropriate class name to the `:root` selector, and modify the colors as desided. Two additional examples (`highcontrast` and `dark`) are provided by default in[`assets/css/colorschemes.css`](https://github.com/qgis/qwc2-demo-app/blob/master/static/assets/css/colorschemes.css).

You can then modify the color scheme which is applied by default by setting `defaultColorScheme` in `config.json` to an appropriate class name (i.e. `highcontrast` or `dark`).

To change the color scheme at runtime in QWC2, make sure the `Settings` plugin is enabled, and in the `Settings` plugin configuration block in `config.json` list the color schemes below `colorSchemes`. Refer to the [sample `config.json`](https://github.com/qgis/qwc2-demo-app/blob/master/static/config.json).

*Note*: When changing the color scheme via Settings dialog in QWC2, the picked color scheme is stored in the browser local storage, and this setting will override the `defaultColorScheme` setting from `config.json`. Specifying the `style` URL-parameter (see [URL parameters](../topics/Interfacing.md#url-parameters)) will take precedence over all other settings.

*Note:* Make sure that `assets/css/colorschemes.css` is included in `index.html`.

### Overriding component styles

Occasionally, it may be desired to customize the styling on the QWC2 components. The recommended approach is to add the corresponding style overrides to `assets/css/qwc2.css`.

*Note:* Make sure that `assets/css/qwc2.css` is included in `index.html`.

### Customizing the application logo

The application logo in its various shapes and sizes are located below `assets/img/`. In particular, the `logo.svg` and `logo-mobile.svg` images are displayed as in the top left corner of QWC2 in desktop and mobile mode respectively. If you'd like to use another format than SVG (while keeping `logo` and `logo-mobile` as base name), you can change `logoFormat` in the `TopBar` configuration block in `config.json`.

### Providing custom map thumbnails

By default, when generating the themes configuration (see [ThemesConfiguration.md#generating-theme-configuration]), a default map thumbnail is generating via WMS `GetMap`, and placed below `assets/img/genmapthumbs`. You can provide your own thumbnail images instead by placing the corresponding images below `assets/img/mapthumbs` and referencing these as `thumbnail` in you theme configuration block in [`themesConig.json`](ThemesConfiguration.md#writing-themes-configuration).

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

QWC2 is divided into two repositories:

- The QWC2 components, hosted at [https://github.com/qgis/qwc2/](https://github.com/qgis/qwc2/). This repository contains the core building blocks common to all QWC2 applications.
- The QWC2 application, the demo application is hosted at [https://github.com/qgis/qwc2-demo-app](https://github.com/qgis/qwc2-demo-app).

To build a custom viewer, the first step is cloning the demo application:
```bash
git clone --recursive https://github.com/qgis/qwc2-demo-app.git qwc2-app
```
The typical layout of a QWC2 app source tree is as follows:

| Path                         | Description
|------------------------------|---------------------------------------------------------------------|
|`├─ static/`                  |                                                                     |
|`│  ├─ assets/`               | See [Viewer assets](#viewer-assets)                                 |
|`│  ├─ translations/`         | Translation files.                                                  |
|`│  ├─ config.json`           | Master configuration file.                                          |
|`│  └─ themes.json`           | Full theme configuration, autogenerated from `themesConfig.json`.   |
|`├─ js/`                      |                                                                     |
|`│  ├─ app.jsx`               | Entry point of the ReactJS application.                             |
|`│  ├─ appConfig.js`          | Configuration of the qwc2 core modules.                             |
|`│  ├─ Help.jsx`              | Built-in component of custom Help dialog, see [Help dialog](#help-dialog). |
|`│  └─ SearchProviders.js`    | Built-in custom search providers, see [Search providers](#search-providers). |
|`├─ icons/`                   | Application icons.                                                |
|`├─ qwc2/`                    | Git submodule containing the core qwc2 components.                |
|`├─ index.html`               | Entry point.                                                      |
|`├─ package.json`             | NodeJS configuration file.                                        |
|`├─ themesConfig.json`        | Themes configuration.                                             |
|`└─ webpack.config.js`        | Webpack configuration.                                            |

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
When using `qwc-docker`, copy the contents of the `qwc2-app/prod` folder to `qwc-docker/volumes/qwc2` and edit the `qwc-docker/docker-compose.yml` to use `qwc-map-viewer-base` with your custom build:
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
### Keeping the QWC2 application up to date

As mentioned above, QWC2 is split into a common components repository and an application specific repository. The goal of this approach is to cleanly separate user-specific configuration and components which common components which serve as a basis for all QWC2 applications, and to make it as easy as possible to rebase the application onto the latest common QWC2 components.

The recommended workflow is to keep the `qwc2` folder a submodule referencing the [upstream qwc2 repository](https://github.com/qgis/qwc2). To update it, just checkout/update the desired branch:
```bash
cd qwc2
git checkout master
# or
git checkout YYYY-lts
git pull
```
The [QWC2 Upgrade Notes](../release_notes/QWC2UpgradeNotes.md) documents major changes, and in particular all incompatible changes between releases which require changes to the application specific code and/or configuration.


## Translations <a name="translations"></a>

This section gives an overview of the common tasks related to the QWC2 translations.

### Switching language

By default, QWC2 will attempt to load the translation matching your browser language. Alternatively, you can explicitly specify the language by adding the `lang=<lang>` query parameter to the application URL, i.e. `lang=de-CH`.

The [`Settings`](../references/qwc2_plugins.md#settings) furthermore allows graphically switching the language within QWC2, with the list of available languages configured via the `languages` plugin configuration property.

### Adding and modify translations

When working inside a `qwc2-app` source folder, the translations can be found on two levels:

- At QWC2 components level, in `qwc2-app/qwc2/translations`.
- At application level, in `qwc2-app/static/translations`.

A script will take care of merging the component translations into the application translations. This way, when updating the QWC2 submodule, new translations are automatically obtained. This script is automatically invoked on `yarn start`, but can also be manually invoked using

    yarn run tsupdate

Translations are stored inside the respective `translations` folder as regular plain-text JSON files, named `<lang>.json` and can be freely edited with any text editor.

The `tsconfig.json` files stored inside the respective `translations` folder contains the list of languages for which translations should be generated and a list of message IDs to include in the translation. The `tsupdate` script will automatically scan the code for message IDs (looking for static strings passed to `LocaleUtils.tr` and `LocaleUtils.trmsg`), store these in `tsconfig.json` and automatically create resp. update the translation files.

In some cases `tsconfig.json` will not pick up a message ID (for instance, if it is computed at runtime). In these cases, the message IDs can be added manually to the `extra_strings` section of the `tsconfig.json`.

Also it may be desired to override a translation inherited from the QWC2 components at application level. To prevent `tsupdate` from continuously reverting the overridden translation, the respective message IDs can be added to the `overrides` section in the application `tsconfig.json` file.

To add a new language, list it in `qwc2-app/qwc2/translations/tsconfig.json` and run `yarn run tsupdate`, then complete the messages taking the english translation file as reference.

When adding or modifying translations at QWC2 components level, please contribute them by submitting a pull request to the [upstream qwc2 repository](https://github.com/qgis/qwc2).

### Selectively overriding translation strings

Occasionally, it is desireable to selectively override specific translation strings. While one can modify the full translation file as described above, especially when using the `qwc-map-viewer-demo` docker image, it is easier to just selectively override the desired translation strings and leave the original file unchanged and avoid having to compile a custom viewer (or overwriting the entire file with a docker volume mount).

To do this:

* Set `loadTranslationOverrides` to `true` in `config.json`.
* Create a `<lang>_overrides.json` containing just the ovverridden strings, for example `en-US_overrides.json`:
```json
{
  "messages": {
    "appmenu": {
      "items": {
        "LayerTree": "Layers"
      }
    }
  }
}
```
* Place this file inside the `translations` folder of your production build. When using `qwc-docker`, you can place this file in `qwc-docker/volumes/qwc2/translations/` and mount this file inside the container, i.e. :
```yml
qwc-map-viewer:
  image: sourcepole/qwc-map-viewer-demo:vYYYY.MM.DD
  [...]
  volumes:
    - ./volumes/qwc2/translations/en-US_overrides.json:/qwc2/translations/en-US_overrides.json:ro
```
### Specifying the default fallback translation

When no translation exists for the requested language (i.e. the current browser language), QWC2 will fall back to the default translation specified as `defaultLocaleData` in `qwc2-app/js/appConfig.js`. For the demo viewer, the default fallback translation is `en-US`.
