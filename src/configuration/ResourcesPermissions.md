# Managing Users, Resources and Permissions

`qwc-docker` has a [QWC configuration backend](https://github.com/qwc-services/qwc-admin-gui). That backend can be reached by default at <http://localhost:8088/qwc_admin>.

The configuration backend allows to assign users and groups to roles. The roles in their turn can receive permissions on resources. These configuration settings will be stored in the [configuration database](https://github.com/qwc-services/qwc-base-db). Out of the box `qwc-docker` comes with with a container `qwc-postgis` that contains the configuration database.

## Users, groups and roles

Roles can be given permissions on resources. That means that if you want to give users or groups permissions on resources, then you have to first create a role, configure the permissions that the roles has on some resources, and then assign the role the users or groups.

## Resources

The following resource types are available:

| Resource name          | Description                                                                                 |
|------------------------|---------------------------------------------------------------------------------------------|
| `Map`                  | WMS service corresponding to a QGIS Project, see [Map permissions](#map-permissions).       |
| `├─ Layer`             | Layer of a map.                                                                             | 
| `│  ╰─ Attribute`      | Layer attribute.                                                                            |
| `├─ Data`              | Dataset, for Editing, Feature Form, Attribute Table.                                        |
| `│  ╰─ Attribute`      | Attribute of a dataset.                                                                     |
| `├─ Data (create)`     | Dataset for creating features.                                                              |
| `├─ Data (update)`     | Dataset for updating features.                                                              |
| `├─ Data (delete)`     | Dataset for deleting features.                                                              |
| `├─ Print template`    | Print composer template of a QGIS Project.                                                  |
| `╰─ 3D Tiles Tileset`  | 3D tiles tileset, see [3D view](../topics/View3D.md).                                       |
| `FeatureInfo service`  | Feature info service, see [Info permissions](../topics/FeatureInfo.md#identify-permissions).|
| `╰─ FeatureInfo layer` | Feature info layer.                                                                         |
| `   ╰─ Attribute`      | Attribute of an info layer.                                                                 |
| `WFS Service`          | WFS service, corresponding to a QGIS Project, see [WFS permissions](#wfs-permissions).      |
| `├─ WFS Layer`         | WFS layer.                                                                                  |
| `│  ╰─ Attribute`      | Attribute of a WFS layer.                                                                   |
| `├─ WFS Layer (create)`| WFS layer for creating features.                                                            |
| `├─ WFS Layer (update)`| WFS layer for updating features.                                                            |
| `╰─ WFS Layer (delete)`| WFS layer for deleting features.                                                            |
| `Search facet`         | Fulltext search facet, see [Search permissions](../topics/Search.md#search-permissions).    |
| `Viewer task`          | Viewer task key, see [Viewer task permissions](#viewer-task-permissions).                   |
| `Document template`    | Document template name, see [Report permissions](../topics/Reports.md#Permissions).         |
| `Theme info link`      | Theme info link name, see [theme info links](ThemesConfiguration.md#theme-info-links).      |
| `Plugin`               | Plugin name of [Plugin data](ThemesConfiguration.md#plugin-data) entries.                   |
| `╰─ Plugin data`       | Plugin resource name [Plugin data](ThemesConfiguration.md#plugin-data) entries.             |

*Note*: New resource types, i.e. for custom QWC plugins, can be inserted into the `qwc_config.resource_types` table of the QWC configuration database..

## Permissions

Permissions are based on roles. Roles can be assigned to groups or users, and users can be members of groups.
A special role is `public`. The `public` role always applies, no matter whether a user is signed in or is not signed in.

Roles can be assigned permission for resources.

The `write` flag is only used for `Data` and `WFS Layer` resources and determines whether the dataset / WFS layer is read-only or writeable (the respective  `create` / `update` / `delete` allow for fine-grained CRUD permission control).

By using the `permissions_default_allow` configuration setting in `tenantConfig.json`, some resources can be set to be permitted or restricted by default if no permissions are set (default: `false`). Among affected resources are `Map`, `Layer`, `Print template`, `Viewer task`, `FeatureInfo service`, `FeatureInfo layer`. E.g.:

* `permissions_default_allow=true`: all maps and layers are permitted by default
* `permissions_default_allow=false`: maps and layers are only available if their resources and permissions are explicitly configured

Based on the user's identity (user name and/or group name), all corresponding roles and their permissions and restrictions are collected from the QWC configuration database by the [QWC Config Generator](https://github.com/qwc-services/qwc-config-generator), which then generates a `permissions.json` file.

The QWC services will read the `permissions.json` to filter the responses according to these permissions and restrictions, by using `PermissionClient::resource_permissions()` or `PermissionClient::resource_restrictions()` from [QWC Services Core](https://github.com/qwc-services/qwc-services-core).

### Map permissions<a name="map-permissions"></a>

The `Map` resource permissions control whether a theme is visibile and whether the corresponding `WMS` is accessible via `qwc-ogc-service`. The name of a `Map` resource corresponds to the relative path to the project below `qgs-resources` without `.qgs` extension (so i.e. the resource name for `qgs-resources/subfolder/project.qgs` will be `subfolder/project`).

*Note*: The display behaviour of restricted themes can be customized with the following settings in the `mapViewer` service config in `tenantConfig.json`:

* `show_restricted_themes`: Whether to show placeholder items for restricted themes. Default: `false`.
* `show_restricted_themes_whitelist`: Whitelist of restricted theme names to display as placeholders. If empty, all restricted themes are shown. Only used if  `show_restricted_themes` enabled. Default: `[]`.
* `redirect_restricted_themes_to_auth`: Whether to redirect to login on auth service if requesting a restricted theme in URL params, if not currently signed in. Default: `false`.

The `Layer` resource permissions control whether a theme layer is visibile and whether it is exposed via `WMS` by the `qwc-ogc-service`. The name of the `Layer` resource corresponds to the QGIS layer name, or its WMS short name, if one is set in the QGIS layer properties. 

The `Layer → Attribute` resource permissions control whether a layer attribute is visibile in the WMS GetFeatureInfo results. The name of the `Attribute` resource corresponds to the QGIS field name (not its alias).

The `Print template` resource permissions control access to a QGIS print layout. The name of the `Print template` resource is the name of the QGIS print layout.

`Map`, `Layer`, `Attributes`, `Print template` and `3D Tiles Tileset` resources are permitted by default if `permissions_default_allow` is `true`.

The `Data` and subordinate `Attribute` resources control whether access to a dataset is permitted via the [qwc-data-service](https://github.com/qwc-services/qwc-data-service). `Data` resources are not permitted by default. They are used for controlling the dataset accessible for [Editing](../topics/Editing.md) and by the [FeatureForm](../topics/FeatureInfo.md#feature-form).

For more detailed [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) permissions `Data (create)`, `Data (update)` and `Date (delete)` can be used instead of `Data`. A `Data` permission with `write=true` permits all CRUD operations.

## Viewer task permissions<a name="viewer-task-permissions"></a>

The `Viewer task` resource defines viewer functionalities (e.g. `Print` or `MapExport`) that can be restricted or permitted.

The resource name will be matched against:

- The `key` in `menuItems` and `toolbarItems` in the QWC `config.json`.
- The `name` of a plugin entry in `config.json`.
- The `task` configuration property of a `TaskButton` plugin entry in `config.json`

*Note*: You can restrict tasks entires which specify a mode (i.e. `{"key": "Measure", "mode": "LineString"}`) by concatenating the task key and the mode as the `viewer_task` resource name, i.e. `MeasureLineString`.

Restricted viewer task items are then removed from the menu and toolbar in the map viewer.

## WFS/OAPIF permissions<a name="wfs-permissions"></a>

WFS and OGC API Features (OAPIF) services are disabled by default and need to be explicitly permitted to be exposed by the `qwc-ogc-service`. The services also need to be published in in `QGIS → Project Properties → QGIS Server → WFS/OAPIF`.

The `WFS Service` resource permissions control whether a WFS service is exposed by the `qwc-ogc-service`. If a `WFS Service` is permitted, all its (published) child layers are permitted by default, without write permissions.

The `WFS Layer` resource permissions allow individually controlling whether child layers of a `WFS Service` are permitted and writable (via WFS-T or OAPIF). Aditionally, the `WFS Layer (create)`, `WFS Layer (update)` and `WFS Layer (delete)` resource permissions allow setting fine-grained CRUD permissions on the `WFS Layer`.

The `WFS Layer → Attribute` resource permissions allow controlling whether a WFS layer attribute is exposed via `qwc-ogc-service`.

## Group registration

Using the optional [Registration GUI](https://github.com/qwc-services/qwc-registration-gui) allows users to request membership or unsubscribe from registrable groups. These requests can then be accepted or rejected in the [Admin GUI](https://github.com/qwc-services/qwc-admin-gui).

Workflow:

* Admin GUI
  * admin user creates new groups with assigned roles and permissions on resources
  * admin user configures registrable groups
* Registration GUI
  * user select desired groups from registrable groups and submits application form
  * admin users are notified of new registration requests
* Admin GUI
  * admin user selects entry from list of pending registration requests
  * admin user accepts or rejects registration requests for a user
  * user is added to or removed from accepted groups
  * user is notified of registration request updates
* Map Viewer
  * user permissions are updated for new groups

