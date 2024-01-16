# ChangeLog

This file lists the most important changes in QWC2 and qwc-services between LTS releases.

## 2023-lts &rarr; 2024-lts

### Upgrade notes

When upgrading from a 2023-lts setup, please note the entries marked with *\[2023-lts &rarr; 2024-lts\]* in the upgrade notes:

* [QWC2 upgrade notes](./QWC2UpgradeNotes.md)
* [qwc-docker upgrade notes](./QwcDockerUpgradeNotes.md)

### General

* [Support common plugin configuration applied to both mobile and desktop](https://qwc-services.github.io/2024-lts/configuration/ViewerConfiguration/#plugin-configuration)
* [Support resource syntax in background layer definitions](https://qwc-services.github.io/2024-lts/configuration/ThemesConfiguration/#background-layers)
* [Support per-theme `startupTask`](https://qwc-services.github.io/2024-lts/configuration/ViewerConfiguration/#global-settings-overridable-per-theme)
* [Support spearate mobile/desktop sections for toplevel config properties](https://qwc-services.github.io/2024-lts/configuration/ViewerConfiguration/#separate-mobile-desktop-global-settings)
* [Add support for tenantConfig templates](https://qwc-services.github.io/2024-lts/topics/MultiTenancy/#tenantconfig-template)
* [Add config option for redirect to login if requesting a restricted theme](https://qwc-services.github.io/2024-lts/configuration/ResourcesPermissions/#restricted-themes)
* [Add support for configuring projects stored in database](https://qwc-services.github.io/2024-lts/configuration/ThemesConfiguration/#projects-in-database)
* [Add support for qgz projects](https://qwc-services.github.io/2024-lts/configuration/ThemesConfiguration/#using-the-qgz-project-file-format)

### Editing

* Display clickable in editable text fields
* Allow generating nested 1:N relation forms (see [`generate_nested_nrel_forms`](https://qwc-services.github.io/2024-lts/topics/Editing/#1n-relations))
* Joined fields as configured in QGIS the project are now handled by the `qwc-data-service`

### FeatureInfo

* [Allow specifying a info template path rather than requiring to specify the template inline](https://qwc-services.github.io/2024-lts/topics/FeatureInfo/#custom-html-templates)

### HeightProfile

* [Allow printing height profile](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#heightprofile)

### LayerTree

* Allow importing GeoPDF files
* Allow zooming to layer groups
* Allow setting group transparency
* Add support for switching WMS layer styles

### Map

* Show a warning when attempting to load a non-existent theme, theme layer or background layer
* Allow individually controlling snapping to vertex/edge
* Snap to all vector layers: Redlining, GeoJSON, KML, WFS (see also [`wfs_max_scale`](https://qwc-services.github.io/2024-lts/topics/Snapping/))
* [Support external MVT layers](https://qwc-services.github.io/2024-lts/configuration/ThemesConfiguration/#external-layers)

### Print

* [Add support for atlas printing](https://qwc-services.github.io/2024-lts/topics/Printing/#print-atlas)
* [Add GeoPDF support](https://qwc-services.github.io/2024-lts/topics/Printing)
* Support layer resource URIs as `printLayer` (i.e. `wms:https://wms.geo.admin.ch#ch.are.bauzonen`)
* [Improved print label configuration in `printLabelConfig`](https://qwc-services.github.io/2024-lts/configuration/ThemesConfiguration/)
* [Add support for print layout templates](https://qwc-services.github.io/2024-lts/topics/Printing/#layout-templates)

### Redlining

* Add redlining support for squares, rectangles, ellipses and transform tool to scale/rotate
* Allow displaying measurements while drawing
* Add numeric input widget
* Support line end arrow heads
* Add GeoJSON/KML export

### Search

* [New QGIS feature search provider](https://qwc-services.github.io/2024-lts/topics/Search/#configuring-the-qgis-feature-search)
* [Provider/geometry filtering to search box](https://qwc-services.github.io/2024-lts/topics/Search/#filtering)
* Allow configuring search highlight style (see [`searchOptions.highlightStyle`](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#topbar))

### Settings

* [Allow setting default startup theme/bookmark for logged in user](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#settings)

### Share

* Permalink expiry date (see [`default_expiry_period`](https://qwc-services.github.io/2024-lts/references/qwc-permalink-service/))
* Allow copying QR code to clipboards on supported browsers

### New plugins

* [Cyclomedia](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#cyclomedia)
* [QGIS FeatureSearch](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#featuresearch)
* [MapExport](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#mapexport) (replacement for `RasterExport` and `DxfExport`)
* [MapLegend](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#maplegend)
* [NewsPopup](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#newspopup)
* [Routing](https://qwc-services.github.io/2024-lts/references/qwc2_plugins/#routing)


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
