# Managing Users, Resources and Permissions

`qwc-docker` has a [QWC configuration backend](https://github.com/qwc-services/qwc-admin-gui). That backend can be reached by default at <http://localhost:8088/qwc_admin>.

The configuration backend allows to assign users and groups to roles. The roles in their turn can receive permissions on resources. These configuration settings will be stored in the [configuration database](https://github.com/qwc-services/qwc-config-db). Out of the box `qwc-docker` comes with with a container `qwc-postgis` that contains the configuration database.

## Users, groups and roles

All resource permissions are assigned to a role. On their part, you can assign a user and a group of users to a role.

## Resources

The following resource types are available:

* `Map`: WMS corresponding to a QGIS Project
  * `Layer`: layer of a map
    * `Attribute`: attribute of a map layer
  * `Print template`: print composer template of a QGIS Project
  * `Data`: Data layer for editing
    * `Attribute`: attribute of a data layer
  * `Data (create)`: Data layer for creating features
  * `Data (read)`: Data layer for reading features
  * `Data (update)`: Data layer for updating features
  * `Data (delete)`: Data layer for deleting features
* `Viewer`: custom map viewer configuration
* `Viewer task`: permittable viewer tasks
* `FeatureInfo service`: Feature info service
  * `FeatureInfo layer`: Feature info layer
    * `Attribute`: attribute of a feature info layer

The resource name corresponds to the technical name of its resource (e.g. WMS layer name). Most notably, the name of a `map` resource corresponds to the relative path to the project below `qgs-resources` without `.qgs` extension (so i.e. the resource name for `qgs-resources/subfolder/project.qgs` will be `subfolder/project`).

*Note:* If your QGIS project is configured to return the field aliases rather than the field names in `GetFeatureInfo`, the resource name for layer `attribute` resources corresponds to the alias of the field.

Available `map`, `layer`, `attribute` and `print_template` resources are determined from WMS `GetProjectSettings` and the QGIS projects.

`data` and their `attribute` resources define a data layer for the [Data service](https://github.com/qwc-services/qwc-data-service).

For more detailed [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) permissions `data_create`, `data_read`, `data_update` and `data_delete` can be used instead of `data`
(`data` and `write=False` is equivalent to `data_read`; `data` and `write=True` is equivalent to all CRUD resources combined).

The `viewer` resource defines a custom viewer configuration for the map viewer (see [Custom viewer configurations](https://github.com/qwc-services/qwc-map-viewer#custom-viewer-configurations)).

The `viewer_task` resource defines viewer functionalities (e.g. printing or raster export) that can be restricted or permitted.
Their `name` (e.g. `RasterExport`) corresponds to the `key` in `menuItems` and `toolbarItems` in the QWC2 `config.json`. Restricted viewer task items are then removed from the menu and toolbar in the map viewer. Viewer tasks not explicitly added as resources are kept unchanged from the `config.json`.

*Note*: The resource types, i.e. for custom QWC2 plugins, can be extended by inserting new types into the `qwc_config.resource_types` table.
These can be queried, e.g. in a custom service, by using `PermissionClient::resource_permissions()` or
`PermissionClient::resource_restrictions()` from [QWC Services Core](https://github.com/qwc-services/qwc-services-core).

## Permissions

Permissions are based on roles. Roles can be assigned to groups or users, and users can be members of groups.
A special role is `public`, which is always included, whether a user is signed in or not.

Each role can be assigned a permission for a resource.

The `write` flag is only used for `data` resources and sets whether a data layer is read-only.

Based on the user's identity (user name and/or group name), all corresponding roles and their permissions and restrictions are collected.
The service configurations are then modified according to these permissions and restrictions.

Using the `permissions_default_allow` configuration setting in `tenantConfig.json`, some resources can be set to be permitted or restricted by default if no permissions are set (default: `false`). Among affected resources are `Map`, `Layer`, `Print template`, `Viewer task`, `FeatureInfo service`, `FeatureInfo layer`. E.g.:

* `permissions_default_allow=true`: all maps and layers are permitted by default
* `permissions_default_allow=false`: maps and layers are only available if their resources and permissions are explicitly configured

## Restricted themes

The display behaviour of restricted themes can be configured in the `mapViewer` service configuration in `tenantConfig.json` as follows:
```json
{
  "name": "mapViewer",
  "config": {
    "show_restricted_themes": false,
    "show_restricted_themes_whitelist": [],
    "redirect_restricted_themes_to_auth": false,
    "internal_permalink_service_url": "http://qwc-permalink-service:9090"
  }
}
```
* `show_restricted_themes`: Whether to show placeholder items for restricted themes. Default: `false`.
* `show_restricted_themes_whitelist`: Whitelist of restricted theme names to display as placeholders. If empty, all restricted themes are shown. Only used if  `show_restricted_themes` enabled. Default: `[]`.
* `redirect_restricted_themes_to_auth`: Whether to redirect to login on auth service if requesting a restricted theme in URL params, if not currently signed in. Default: `false`.
* `internal_permalink_service_url`: Internal permalink service URL for getting the theme from a resolved permalink for redirecting to login (default: `http://qwc-permalink-service:9090`). This is used only if `redirect_restricted_themes_to_auth` is enabled and `permalink_service_url` is set.


## Permissions file

The [QWC Config Generator](https://github.com/qwc-services/qwc-config-generator) generates a JSON file for all permissions from the QWC ConfigDB. See READMEs of QWC services for service specific contents in `permissions.json`.

<!--Alternatively, a simplified permissions format is also supported, see [unified permissions](doc/unified_permissions.md).-->

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

