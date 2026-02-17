# ChangeLog

This file lists the most important changes in QWC and qwc-services between LTS releases.

## 2025-lts &rarr; 2026-lts

When upgrading from a 2025-lts setup, please note the entries marked with *\[2025-lts &rarr; 2026-lts\]* in the upgrade notes:

* [QWC upgrade notes](./QWC2UpgradeNotes.md)
* [qwc-docker upgrade notes](./QwcDockerUpgradeNotes.md)

### General
* QWC is now published on [NPM](https://www.npmjs.com/package/qwc2), which can be used as a dependency for custom QWC builds
* Enchanced keyboard navigation throughout

### Editing
* Dynamically load editConfig for theme layers and imported layers (reduces size of initial `themes.json`, allows editing imported theme layers)
* Add support for virtual (i.e. calculated) fields
* Allow showing measurements while drawing
* Add support for editing attributes of datasets with curve geometries (geometries will be read-only)
* Add support for ValueRelation widgets with multiple selections
* Add support for array field types
* Add support visibility expressions for DnD designer form tabs and group boxes
* Allow editing nested datasets with geometries
* Allow recording GPS position for point/line geometries
* Allow copying compatible attributes when copying existing feature
* Extended [expression grammar](https://github.com/qgis/qwc2/blob/64b3810996ec58f9f0d6247772b56cc86a236186/utils/expr_grammar/grammar.ne)
* Allow hiding hidden fields in [AttributeTable](../references/qwc2_plugins#attributetable)
* The AttributeTable now uses service-side pagination by the `qwc-data-service` for loading the feature collection

### Identify
* Add new paginated display mode, enable via [`resultDisplayMode`](../references/qwc2_plugins#identify) config setting
* Allow comparing selected identify results side-by-side
* Add shapefile and XLSX exporters
* The GeoJSON exporter now exports in `EPSG:4326`

### Layers and LayerTree
* Expose layer visibility presets ("themes"), as configured in the QGIS project, in the LayerTree
* Honour layer refresh interval, as configured in the [QGIS project](../configuration/ThemesConfiguration#create-qgis-project)
* Show control to toggle group and sublayers to LayerTree if [`groupTogglesSublayers`](../references/qwc2_plugins#layertree) is `false`
* Allow adding separators to the LayerTree also if [`flattenGroups`](../references/qwc2_plugins#layertree) is `false`
* Display layer style selector also for group layers in LayerTree

### Localization
* Add support for translated QWC themes, see [Translations](../topics/Translations#translated-themes)
* Add support for `{lang}` placeholder in the [`NewsPopup`](../references/qwc2_plugins#newspopup) `newsDocument` URL
* Add support for `$lang$` placehodler in menu item and identify attribute links
* Add support for `translate(<fieldname>)` to translate field names in [custom HTML info templates](../topics/FeatureInfo/#custom-html-templates)

### Measure
* Allow configuring [line head and tail markers](../references/qwc2_plugins#measure) for distance and bearing measurement geometries
* Allow drawing multiple measurement geometries, see also [`clearMeasurementsOnExit` and `clearMeasurementsOnModeChange`](../references/qwc2_plugins#measure) config settings
* Display total line length next to geometry, also display perimeter length if [`showPerimeterLength`](../references/qwc2_plugins#measure) is set
* Allow specifying custom `ElevationInterface` for [HeightProfile](../references/qwc2_plugins#heightprofile)
* Add support for multiple height profiles returned by [`qwc-elevation-service`](https://github.com/qwc-services/qwc-elevation-service)

### Redlining
* Add support for transform a selection of multiple objects
* Allow cloning selected features
* Allow recording GPS position for point/line drawings
* Allow setting line dash pattern
* Allow setting and editing attributes of redlining features
* Add specturm color picker to color buttons

### Reports
* Allow specifying multiple report templates per layer, see [Reports](../topics/Reports#configuring-the-web-client)
* Add `single_report` mode, to generate one report with all selected features instead of one report per selected feature

### Search
* [QGIS feature search](../topics/Search/#configuring-the-qgis-feature-search): allow dynamically populating selection lists via `options_query`
* Allow searching for catalog layers in main search field, see [`registerCatalogSearchProvider`](../references/qwc2_plugins#layercatalog)
* Allow searching for task menu entries in main search field, see [`registerTaskSearchProvider`](../references/qwc2_plugins#topbar)
* Allow dynamically registering search providers via 
* Allow loading search filter regions from an external file, see [search filtering](../topics/Search/#filtering)

### Other changes
* Bookmark: Rework plugin for improved usabiliy
* Cyclomedia: Update default cyclomediaVersion to 25.7
* GeometryDigitizer: Allow chosing between wkt and geojson as the format for sending geometries to the target application
* MapExport: Include external layers in DXF export and merge result
* Portal, ThemeSwitcher: Introduce `expandGroups` config setting to control whether groups are expanded by default
* Routing: Allow adding routing result as redlining layers
* ThemeSwitcher: Allow displaying active theme
* API: Allow interacting with embedded QWC instances via [`postMessage`](../references/qwc2_plugins#api)

### New plugins
* [ObliqueView](../references/qwc2_plugins#obliqueview), see also [Oblique View](../topics/ObliqueView)
* [ObjectList](../references/qwc2_plugins#objectlist)
* [Panoramax](../references/qwc2_plugins#panoramax)
* [TourGuide](../references/qwc2_plugins#tourguide), see also [Tour Guide](../topics/Tourguide)
* [ValueTool](../references/qwc2_plugins#valuetool)
* [View3D](../references/qwc2_plugins#view3d), see also [3D View](../topics/View3D)

### Services

**qwc-admin-gui**

* Allow aborting config-generator workers
* Allow sending [invitation mails](https://github.com/qwc-services/qwc-admin-gui/?tab=readme-ov-file#invitations)

**qwc-data-service**

* Add support for pagination and sorting for dataset index endpoint
* Optimized queries for querying datasets with joined tables
* New [filter operators](https://github.com/qwc-services/qwc-data-service/?tab=readme-ov-file#filter-expressions): `~, HAS, HAS NOT`

**qwc-document-service**

* Allow using precompiled `*.jasper` templates (if `permit_subreports=true`)
* Keep JVM alive to avoid significant per-request overhead
* Read true font family names from font files instead of relying only on font file name convention

**qwc-elevation-service**

* Allow [configuring](https://github.com/qwc-services/qwc-elevation-service/?tab=readme-ov-file#elevation-service-config) multiple elevation datasets

**qwc-legend-service**

* Allow providing distinct [custom legend images](../topics/LegendGraphics/#providing-custom-legend-images) for layers with multiple styles

**qwc-map-viewer**

* Allow restricting viewer assets via `Viewer Asset` [resource permissions](../configuration/ResourcesPermissions/#viewer-asset-permissions)
* Add `Content-Security-Policy` response header when querying `index.html`

**qwc-ogc-service**

* Add support for WFS-T
* Add support for OGC API Features
* Add a service landing page
* Allow forcing basic auth challenge for WMS/WFS requests via [`REQUIREAUTH` query param](https://github.com/qwc-services/qwc-ogc-service?tab=readme-ov-file#basic-auth)

**qwc-qgis-server**

* Build release-nightly Docker images with more verbose debug output, see [Debugging](https://github.com/qwc-services/qwc-qgis-server#debugging).

**qwc-qgis-server-plugins**

* New [`datasource_filter_username` plugin](https://github.com/qwc-services/qwc-qgis-server-plugins?tab=readme-ov-file#datasource_filter_username)

**qwc-qgs-cache-preseed**

* [New service for pre-seeding the QGIS Server project cache](https://github.com/qwc-services/qwc-qgs-cache-preseed)

### Full changelogs

* [QWC](https://github.com/qgis/qwc2/compare/2025-lts...2026-lts)
* [qwc-3d-tile-info-service](https://github.com/qwc-services/qwc-3d-tile-info-service/compare/a30107c...2026-lts)
* [qwc-admin-gui](https://github.com/qwc-services/qwc-admin-gui/compare/2025-lts...2026-lts)
* [qwc-base-db](https://github.com/qwc-services/qwc-base-db/compare/2025-lts...2026-lts)
* [qwc-config-generator](https://github.com/qwc-services/qwc-config-generator/compare/2025-lts...2026-lts)
* [qwc-data-service](https://github.com/qwc-services/qwc-data-service/compare/2025-lts...2026-lts)
* [qwc-db-auth](https://github.com/qwc-services/qwc-db-auth/compare/2025-lts...2026-lts)
* [qwc-document-service](https://github.com/qwc-services/qwc-document-service/compare/2025-lts...2026-lts)
* [qwc-elevation-service](https://github.com/qwc-services/qwc-elevation-service/compare/2025-lts...2026-lts)
* [qwc-ext-service](https://github.com/qwc-services/qwc-ext-service/compare/2025-lts...2026-lts)
* [qwc-feature-info-service](https://github.com/qwc-services/qwc-feature-info-service/compare/2025-lts...2026-lts)
* [qwc-fulltext-search-service](https://github.com/qwc-services/qwc-fulltext-search-service/compare/2025-lts...2026-lts)
* [qwc-ldap-auth](https://github.com/qwc-services/qwc-ldap-auth/compare/2025-lts...2026-lts)
* [qwc-legend-service](https://github.com/qwc-services/qwc-legend-service/compare/2025-lts...2026-lts)
* [qwc-mapinfo-service](https://github.com/qwc-services/qwc-mapinfo-service/compare/2025-lts...2026-lts)
* [qwc-map-viewer](https://github.com/qwc-services/qwc-map-viewer/compare/2025-lts...2026-lts)
* [qwc-ogc-service](https://github.com/qwc-services/qwc-ogc-service/compare/2025-lts...2026-lts)
* [qwc-permalink-service](https://github.com/qwc-services/qwc-permalink-service/compare/2025-lts...2026-lts)
* [qwc-print-service](https://github.com/qwc-services/qwc-print-service/compare/2025-lts...2026-lts)
* [qwc-qgs-cache-preseed](https://github.com/qwc-services/qwc-qgs-cache-preseed/compare/3e37335..2026-lts)
* [qwc-registration-gui](https://github.com/qwc-services/qwc-registration-gui/compare/2025-lts...2026-lts)
* [qwc-wms-proxy](https://github.com/qwc-services/qwc-wms-proxy/compare/2025-lts...2026-lts)


## 2024-lts &rarr; 2025-lts

### Upgrade notes

When upgrading from a 2024-lts setup, please note the entries marked with *\[2024-lts &rarr; 2025-lts\]* in the upgrade notes:

* [QWC upgrade notes](./QWC2UpgradeNotes.md)
* [qwc-docker upgrade notes](./QwcDockerUpgradeNotes.md)


### Viewer Configuration
* [Config: Allow overriding plugin config per theme](../configuration/ThemesConfiguration#manual-theme-configuration)
* [Allow adding custom plugins via QWC API](../references/qwc2_plugins#api)
* [Allow registering identify exporters and attribute calculators via QWC2 API](../references/qwc2_plugins#api)

### General
* Allow detaching QWC dialogs (i.e. Attribute Table) to separate browser windows
* [Allow specifying OverviewMap layer independent from current background layer](../references/qwc2_plugins#overviewmap)

### Editing / AttributeForm / AttributeTable
* [Honour expressions in QGIS Attributes Form configuration for group box visibility, default value and value-relation filter as defined](../topics/Editing.md#expressions) (currently [limited grammar](https://github.com/qgis/qwc2/blob/2025-lts/utils/expr_grammar/grammar.ne))
* Allow limiting Attibute Table to current map extent
* Add CSV export to Attribute Table
* Highlight hovered / filtered features in Attribute Table

### Redlining
* Add support for rotating labels
* [Allow configuring available tools / default color / unit length](../references/qwc2_plugins#redlining)
* Add CTRL / SHIFT support to transform tool to scale objects from corner / preserving aspect ratio

### Measure
* Show measurement labels in map of height profile print output

### Print
* Reworked plugin with new series print mode

### Layer tree
* Allow importing (zipped) Shapefiles
* [Add option to only show groups](../references/qwc2_plugins#layertree)
* [Add option to show a link to the Attribute Table of a layer](../references/qwc2_plugins#layertree)

### Identify
* Show layer selection and feature count

### New plugins
* [Portal](../references/qwc2_plugins#portal)
* [MapFilter](../references/qwc2_plugins#mapfilter)
* [GeometryDigitizer](../references/qwc2_plugins#geometrydigitizer)
* [Reports](../references/qwc2_plugins#reports) (see also [Reports](../topics/Reports.md))
* [CookiePopup](../references/qwc2_plugins#cookiepopup)

### QWC services
* [Make `qwc_config` schema name configurable](../topics/MultiTenancy.md#multi-tenancy-with-separate-configdb-schemas)

### Config Generator
* Create theme groups for subdirs below scan dir
* Add option to save scanned projects and groups in themes configuration
* Handle template themesConfig section in tenantConfig template
* Allow setting `generate_nested_nrel_forms` per dataset in the theme item editConfig

### Admin GUI
* Allow generating configuration using cached project capabilities
* Allow generating configuation forcing read-only dataset permissions
* Allow querying QGIS Server logs
* Add NewsPopup plugin

### DB Auth
* Allow configuring `post_param_login`, `max_login_attempts`, `totp_enabled`, `totp_issuer_name` in service config
* Display account locked status to user
* Reword reset password to password change, also allow unlocking account
* Introduce `totp_enabled_for_admin` config option
* Implement IP blacklisting
* Add `force_password_change_first_login` config setting

### Data service
* Add recaptcha support for public editing
* Introduce separate `create_user_field` and `create_timestamp_field` for logging record creations
* Honour data source filter as set in the QGIS layer properties

### Document service
* Rewrite, drops the requirement on a separate `jasper-reporting-service`, see [Reports](../topics/Reports.md)

### Feature info service
* Support authentication via basic auth
* Add support for `text/plain`, `text/html` and `application/json` info formats
* [Add support for specifying custom templates by placing a file in `info_templates_path`](../topics/FeatureInfo.md#html-templates)

### Fulltext search service
* [Add trigram search backend](../topics/Search.md#fulltext-search-with-trigram-backend)

### Legend service
* Support authentication via basic auth

### Mapinfo service
* [Support returning multiple values from SQL query to `info_title`](../topics/Mapinfo.md)

### OGC service
* Add support for WFS 1.1.0

### Full changelogs

* [QWC](https://github.com/qgis/qwc2/compare/2024-lts...2025-lts)
* [qwc-admin-gui](https://github.com/qwc-services/qwc-admin-gui/compare/2024-lts...2025-lts)
* [qwc-base-db](https://github.com/qwc-services/qwc-base-db/compare/2024-lts...2025-lts)
* [qwc-config-generator](https://github.com/qwc-services/qwc-config-generator/compare/2024-lts...2025-lts)
* [qwc-data-service](https://github.com/qwc-services/qwc-data-service/compare/2024-lts...2025-lts)
* [qwc-db-auth](https://github.com/qwc-services/qwc-db-auth/compare/2024-lts...2025-lts)
* [qwc-document-service](https://github.com/qwc-services/qwc-document-service/compare/2024-lts...2025-lts)
* [qwc-elevation-service](https://github.com/qwc-services/qwc-elevation-service/compare/2024-lts...2025-lts)
* [qwc-ext-service](https://github.com/qwc-services/qwc-ext-service/compare/2024-lts...2025-lts)
* [qwc-feature-info-service](https://github.com/qwc-services/qwc-feature-info-service/compare/2024-lts...2025-lts)
* [qwc-fulltext-search-service](https://github.com/qwc-services/qwc-fulltext-search-service/compare/2024-lts...2025-lts)
* [qwc-ldap-auth](https://github.com/qwc-services/qwc-ldap-auth/compare/2024-lts...2025-lts)
* [qwc-legend-service](https://github.com/qwc-services/qwc-legend-service/compare/2024-lts...2025-lts)
* [qwc-mapinfo-service](https://github.com/qwc-services/qwc-mapinfo-service/compare/2024-lts...2025-lts)
* [qwc-map-viewer](https://github.com/qwc-services/qwc-map-viewer/compare/2024-lts...2025-lts)
* [qwc-ogc-service](https://github.com/qwc-services/qwc-ogc-service/compare/2024-lts...2025-lts)
* [qwc-permalink-service](https://github.com/qwc-services/qwc-permalink-service/compare/2024-lts...2025-lts)
* [qwc-print-service](https://github.com/qwc-services/qwc-print-service/compare/2024-lts...2025-lts)
* [qwc-registration-gui](https://github.com/qwc-services/qwc-registration-gui/compare/2024-lts...2025-lts)
* [qwc-wms-proxy](https://github.com/qwc-services/qwc-wms-proxy/compare/2024-lts...2025-lts)
* [jasper-reporting-service](https://github.com/qwc-services/jasper-reporting-service/compare/2024-lts...2025-lts)


## 2023-lts &rarr; 2024-lts

### Upgrade notes

When upgrading from a 2023-lts setup, please note the entries marked with *\[2023-lts &rarr; 2024-lts\]* in the upgrade notes:

* [QWC upgrade notes](./QWC2UpgradeNotes.md)
* [qwc-docker upgrade notes](./QwcDockerUpgradeNotes.md)

### General

* [Support common plugin configuration applied to both mobile and desktop](../configuration/ViewerConfiguration.md#plugin-configuration)
* [Support resource syntax in background layer definitions](../configuration/ThemesConfiguration.md#background-layers)
* [Support per-theme `startupTask`](../configuration/ViewerConfiguration.md#global-settings-overridable-per-theme)
* [Support spearate mobile/desktop sections for toplevel config properties](../configuration/ViewerConfiguration.md#separate-mobile-desktop-global-settings)
* [Add support for tenantConfig templates](../topics/MultiTenancy.md#tenantconfig-template)
* [Add config option for redirect to login if requesting a restricted theme](../configuration/ResourcesPermissions.md#restricted-themes)
* [Add support for configuring projects stored in database](../configuration/ThemesConfiguration.md#projects-in-database)
* [Add support for qgz projects](../configuration/ThemesConfiguration.md#using-the-qgz-project-file-format)

### Editing

* Display clickable links in editable text fields
* Allow generating nested 1:N relation forms (see [`generate_nested_nrel_forms`](../topics/Editing.md#1n-relations))
* Joined fields as configured in QGIS the project are now handled by the `qwc-data-service`

### FeatureInfo

* [Allow specifying a info template path rather than requiring to specify the template inline](../topics/FeatureInfo.md#custom-html-templates)

### HeightProfile

* [Allow printing height profile](../references/qwc2_plugins#heightprofile)

### LayerTree

* Allow importing GeoPDF files
* Allow zooming to layer groups
* Allow setting group transparency
* Add support for switching WMS layer styles

### Map

* Show a warning when attempting to load a non-existent theme, theme layer or background layer
* Allow individually controlling snapping to vertex/edge
* Snap to all vector layers: Redlining, GeoJSON, KML, WFS (see also [`wfs_max_scale`](../topics/Snapping.md))
* [Support external MVT layers](../configuration/ThemesConfiguration.md#external-layers)

### Print

* [Add support for atlas printing](../topics/Printing.md#print-atlas)
* [Add GeoPDF support](../topics/Printing.md)
* Support layer resource URIs as `printLayer` (i.e. `wms:https://wms.geo.admin.ch#ch.are.bauzonen`)
* [Improved print label configuration in `printLabelConfig`](../configuration/ThemesConfiguration.md)
* [Add support for print layout templates](../topics/Printing.md#layout-templates)

### Redlining

* Add redlining support for squares, rectangles, ellipses and transform tool to scale/rotate
* Allow displaying measurements while drawing
* Add numeric input widget
* Support line end arrow heads
* Add GeoJSON/KML export

### Search

* [New QGIS feature search provider](../topics/Search.md#configuring-the-qgis-feature-search)
* Theme layer search (see [`searchThemeLayers`](../configuration/ViewerConfiguration.md#global-settings-overridable-per-theme))
* [Provider/geometry filtering to search box](../topics/Search.md#filtering)
* Allow configuring search highlight style (see [`searchOptions.highlightStyle`](../references/qwc2_plugins#topbar))

### Settings

* [Allow setting default startup theme/bookmark for logged in user](../references/qwc2_plugins#settings)

### Share

* Permalink expiry date (see [`default_expiry_period`](../references/qwc-permalink-service.md))
* Allow copying QR code to clipboards on supported browsers

### New plugins

* [Cyclomedia](../references/qwc2_plugins#cyclomedia)
* [QGIS FeatureSearch](../references/qwc2_plugins#featuresearch)
* [MapExport](../references/qwc2_plugins#mapexport) (replacement for `RasterExport` and `DxfExport`)
* [MapLegend](../references/qwc2_plugins#maplegend)
* [NewsPopup](../references/qwc2_plugins#newspopup)
* [Routing](../references/qwc2_plugins#routing)


### Full changelogs

* [QWC](https://github.com/qgis/qwc2/compare/2023-lts...2024-lts)
* [qwc-admin-gui](https://github.com/qwc-services/qwc-admin-gui/compare/2023-lts...2024-lts)
* [qwc-base-db](https://github.com/qwc-services/qwc-base-db/compare/2023-lts...2024-lts)
* [qwc-config-generator](https://github.com/qwc-services/qwc-config-generator/compare/2023-lts...2024-lts)
* [qwc-data-service](https://github.com/qwc-services/qwc-data-service/compare/2023-lts...2024-lts)
* [qwc-db-auth](https://github.com/qwc-services/qwc-db-auth/compare/2023-lts...2024-lts)
* [qwc-document-service](https://github.com/qwc-services/qwc-document-service/compare/2023-lts...2024-lts)
* [qwc-elevation-service](https://github.com/qwc-services/qwc-elevation-service/compare/2023-lts...2024-lts)
* [qwc-ext-service](https://github.com/qwc-services/qwc-ext-service/compare/2023-lts...2024-lts)
* [qwc-feature-info-service](https://github.com/qwc-services/qwc-feature-info-service/compare/2023-lts...2024-lts)
* [qwc-fulltext-search-service](https://github.com/qwc-services/qwc-fulltext-search-service/compare/2023-lts...2024-lts)
* [qwc-ldap-auth](https://github.com/qwc-services/qwc-ldap-auth/compare/2023-lts...2024-lts)
* [qwc-legend-service](https://github.com/qwc-services/qwc-legend-service/compare/2023-lts...2024-lts)
* [qwc-mapinfo-service](https://github.com/qwc-services/qwc-mapinfo-service/compare/2023-lts...2024-lts)
* [qwc-map-viewer](https://github.com/qwc-services/qwc-map-viewer/compare/2023-lts...2024-lts)
* [qwc-ogc-service](https://github.com/qwc-services/qwc-ogc-service/compare/2023-lts...2024-lts)
* [qwc-permalink-service](https://github.com/qwc-services/qwc-permalink-service/compare/2023-lts...2024-lts)
* [qwc-print-service](https://github.com/qwc-services/qwc-print-service/compare/2023-lts...2024-lts)
* [qwc-registration-gui](https://github.com/qwc-services/qwc-registration-gui/compare/2023-lts...2024-lts)
* [qwc-wms-proxy](https://github.com/qwc-services/qwc-wms-proxy/compare/2023-lts...2024-lts)
* [jasper-reporting-service](https://github.com/qwc-services/jasper-reporting-service/compare/2023-lts...2024-lts)
