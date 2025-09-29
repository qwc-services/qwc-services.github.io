# Map info

The map-info popup is provided by the [MapInfoTooltip](../references/qwc2_plugins.md#mapinfotooltip) plugin. It displays a popup when right-clicking any position on the map.

By default, it displayes the picked coordinates.

If the `qwc-elevation-service` [is enabled](../configuration/ServiceConfiguration.md#enabling-services), it also returns the height at the picked position.

If the `qwc-mapinfo-service` is enabled, queries can be configured in the service configuration in `tenantConfig.json` to return additional information. Example:
```json
{
  "name": "mapinfo",
  "config": {
    "queries": [
      {
        "db_url": "postgresql:///?service=qwc_geodb",
        "info_table": "qwc_geodb.ne_10m_admin_0_countries",
        "info_geom_col": "wkb_geometry",
        "info_display_col": "name",
        "info_where": "type = 'Sovereign country'",
        "info_title": "Country",
        "info_id": "country"
      },
      {
        "db_url": "postgresql:///?service=qwc_geodb",
        "info_sql": "SELECT type FROM qwc_geodb.ne_10m_admin_0_countries WHERE ST_contains(wkb_geometry, ST_SetSRID(ST_Point(:x, :y), :srid)) LIMIT 1",
        "info_title": "Type",
        "info_id": "type"
      },
      {
        "db_url": "postgresql:///?service=qwc_geodb",
        "info_sql": "SELECT abbrev, postal, subregion FROM qwc_geodb.ne_10m_admin_0_countries WHERE ST_contains(wkb_geometry, ST_SetSRID(ST_Point(:x, :y), :srid)) LIMIT 1",
        "info_title": ["Abbreviation", "Postal Code", "Subregion"],
        "info_id": "details"
      }
    ]
  }
}
```
* If `info_table`, `info_geom_col`, `info_display_col` and optionally `info_where` are provided, the result obtained from
```sql
    SELECT {info_display_col}
    FROM {info_table}
    WHERE ST_contains({info_table}.{info_geom_col}, ST_SetSRID(ST_Point(:x, :y), :srid)) AND {info_where}
    LIMIT 1;
```
will be returned and displayed in the map-info popup as with title as specified in `info_title`.

* If `info_sql` is provided, the result obtained from the specified query will be returned. Use the `:x`, `:y` and `:srid` placeholders.
* The `info_id` is required if you want to assign permissions to the mapinfo queries, see below.

## Permissions <a name="permissions"></a>

You can assign permissions to the mapinfo queries by creating and permitting `Map info query` resources, which shall be named according to the `info_id` of the query. If `permissions_default_allow` is `true` in `tenatConfig.json`, all mapinfo queries are permitted by default unless a permission is assigned to a specific role.
