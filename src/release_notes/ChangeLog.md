# ChangeLog

This file lists the most important changes in QWC2 and qwc-services between LTS releases.

## 2024-lts &rarr; 2025-lts

### Upgrade notes

When upgrading from a 2025-lts setup, please note the entries marked with *\[2024-lts &rarr; 2025-lts\]* in the upgrade notes:

* [QWC2 upgrade notes](./QWC2UpgradeNotes.md)
* [qwc-docker upgrade notes](./QwcDockerUpgradeNotes.md)


### Viewer Configuration
* [Config: Allow overriding plugin config per theme](../../configuration/ThemesConfiguration.md#manual-theme-configuration)
* [Allow adding custom plugins via QWC2 API](../../references/qwc2_plugins.md#api)
* [Allow registering identify exporters and attribute calculators via QWC2 API](../../references/qwc2_plugins.md#api)

### General
* Allow detaching QWC2 dialogs (i.e. Attribute Table) to separate browser windows
* [Allow specifying OverviewMap layer independent from current background layer](../../references/qwc2_plugins.md#overviewmap)

### Editing / AttributeForm / AttributeTable
* [Honour expressions in QGIS Attributes Form configuration for group box visibility, default value and value-relation filter as defined](../../topics/Editing.md#expressions) (currently [limited grammar](https://github.com/qgis/qwc2/blob/2025-lts/utils/expr_grammar/grammar.ne))
* Allow limiting Attibute Table to current map extent
* Add CSV export to Attribute Table
* Highlight hovered / filtered features in Attribute Table

### Redlining
* Add support for rotating labels
* [Allow configuring available tools / default color / unit length](../../references/qwc2_plugins.md#redlining)
* Add CTRL / SHIFT support to transform tool to scale objects from corner / preserving aspect ratio

### Measure
* Show measurement labels in map of height profile print output

### Print
* Reworked plugin with new series print mode

### Layer tree
* Allow importing (zipped) Shapefiles
* [Add option to only show groups](../../references/qwc2_plugins.md#layertree)
* [Add option to show a link to the Attribute Table of a layer](../../references/qwc2_plugins.md#layertree)

### Identify
* Show layer selection and feature count

### New plugins
* [Portal](../../references/qwc2_plugins.md#portal)
* [MapFilter](../../references/qwc2_plugins.md#mapfilter)
* [GeometryDigitizer](../../references/qwc2_plugins.md#geometrydigitizer)
* [Reports](../../references/qwc2_plugins.md#reports) (see also [Reports](../../topics/Reports.md))
* [CookiePopup](../../references/qwc2_plugins.md#cookiepopup)

### QWC services
* [Make `qwc_config` schema name configurable](../../topics/MultiTenancy.md#multi-tenancy-with-separate-configdb-schemas)

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
* Rewrite, drops the requirement on a separate `jasper-reporting-service`, see [Reports](../../topics/Reports.md)

### Feature info service
* Support authentication via basic auth
* Add support for `text/plain` and `text/html` info formats

### Fulltext search service
* [Add trigram search backend](../../topics/Search.md#fulltext-search-with-trigram-backend)

### Legend service
* Support authentication via basic auth

### Mapinfo service
* [Support returning multiple values from SQL query to `info_title`](../../topics/Mapinfo.md)

### OGC service
* Add support for WFS 1.1.0

### Full changelogs

* [QWC2](https://github.com/qgis/qwc2/compare/2024-lts...2025-lts)
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

* [QWC2 upgrade notes](./QWC2UpgradeNotes.md)
* [qwc-docker upgrade notes](./QwcDockerUpgradeNotes.md)

### General

* [Support common plugin configuration applied to both mobile and desktop](../../configuration/ViewerConfiguration.md#plugin-configuration)
* [Support resource syntax in background layer definitions](../../configuration/ThemesConfiguration.md#background-layers)
* [Support per-theme `startupTask`](../../configuration/ViewerConfiguration.md#global-settings-overridable-per-theme)
* [Support spearate mobile/desktop sections for toplevel config properties](../../configuration/ViewerConfiguration.md#separate-mobile-desktop-global-settings)
* [Add support for tenantConfig templates](../../topics/MultiTenancy.md#tenantconfig-template)
* [Add config option for redirect to login if requesting a restricted theme](../../configuration/ResourcesPermissions.md#restricted-themes)
* [Add support for configuring projects stored in database](../../configuration/ThemesConfiguration.md#projects-in-database)
* [Add support for qgz projects](../../configuration/ThemesConfiguration.md#using-the-qgz-project-file-format)

### Editing

* Display clickable links in editable text fields
* Allow generating nested 1:N relation forms (see [`generate_nested_nrel_forms`](../../topics/Editing.md#1n-relations))
* Joined fields as configured in QGIS the project are now handled by the `qwc-data-service`

### FeatureInfo

* [Allow specifying a info template path rather than requiring to specify the template inline](../../topics/FeatureInfo.md#custom-html-templates)

### HeightProfile

* [Allow printing height profile](../../references/qwc2_plugins.md#heightprofile)

### LayerTree

* Allow importing GeoPDF files
* Allow zooming to layer groups
* Allow setting group transparency
* Add support for switching WMS layer styles

### Map

* Show a warning when attempting to load a non-existent theme, theme layer or background layer
* Allow individually controlling snapping to vertex/edge
* Snap to all vector layers: Redlining, GeoJSON, KML, WFS (see also [`wfs_max_scale`](../../topics/Snapping.md))
* [Support external MVT layers](../../configuration/ThemesConfiguration.md#external-layers)

### Print

* [Add support for atlas printing](../../topics/Printing.md#print-atlas)
* [Add GeoPDF support](../../topics/Printing.md)
* Support layer resource URIs as `printLayer` (i.e. `wms:https://wms.geo.admin.ch#ch.are.bauzonen`)
* [Improved print label configuration in `printLabelConfig`](../../configuration/ThemesConfiguration.md)
* [Add support for print layout templates](../../topics/Printing.md#layout-templates)

### Redlining

* Add redlining support for squares, rectangles, ellipses and transform tool to scale/rotate
* Allow displaying measurements while drawing
* Add numeric input widget
* Support line end arrow heads
* Add GeoJSON/KML export

### Search

* [New QGIS feature search provider](../../topics/Search.md#configuring-the-qgis-feature-search)
* Theme layer search (see [`searchThemeLayers`](../../configuration/ViewerConfiguration.md#global-settings-overridable-per-theme))
* [Provider/geometry filtering to search box](../../topics/Search.md#filtering)
* Allow configuring search highlight style (see [`searchOptions.highlightStyle`](../../references/qwc2_plugins.md#topbar))

### Settings

* [Allow setting default startup theme/bookmark for logged in user](../../references/qwc2_plugins.md#settings)

### Share

* Permalink expiry date (see [`default_expiry_period`](../../references/qwc-permalink-service.md))
* Allow copying QR code to clipboards on supported browsers

### New plugins

* [Cyclomedia](../../references/qwc2_plugins.md#cyclomedia)
* [QGIS FeatureSearch](../../references/qwc2_plugins.md#featuresearch)
* [MapExport](../../references/qwc2_plugins.md#mapexport) (replacement for `RasterExport` and `DxfExport`)
* [MapLegend](../../references/qwc2_plugins.md#maplegend)
* [NewsPopup](../../references/qwc2_plugins.md#newspopup)
* [Routing](../../references/qwc2_plugins.md#routing)


### Full changelogs

* [QWC2](https://github.com/qgis/qwc2/compare/2023-lts...2024-lts)
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
