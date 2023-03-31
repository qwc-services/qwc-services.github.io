+++
menuTitle = "qwc-permalink-service"
weight = 5
+++
# QWC Permalink Service

- [1. Property `QWC Permalink Service > $schema`](#$schema)
- [2. Property `QWC Permalink Service > service`](#service)
- [3. Property `QWC Permalink Service > config`](#config)
  - [3.1. Property `QWC Permalink Service > config > db_url`](#config_db_url)
  - [3.2. Property `QWC Permalink Service > config > permalinks_table`](#config_permalinks_table)
  - [3.3. Property `QWC Permalink Service > config > user_permalink_table`](#config_user_permalink_table)
  - [3.4. Property `QWC Permalink Service > config > bookmarks_sort_order`](#config_bookmarks_sort_order)

**Title:** QWC Permalink Service

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [$schema](#$schema ) | No      | string | No         | -          | JSON Schema       |
| + [service](#service ) | No      | const  | No         | -          | Service name      |
| + [config](#config )   | No      | object | No         | -          | Config options    |

## <a name="$schema"></a>1. Property `QWC Permalink Service > $schema`

**Title:** JSON Schema

|              |                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Type**     | `string`                                                                                                           |
| **Required** | No                                                                                                                 |
| **Format**   | `uri`                                                                                                              |
| **Default**  | `"https://raw.githubusercontent.com/qwc-services/qwc-permalink-service/master/schemas/qwc-permalink-service.json"` |

**Description:** Reference to JSON schema of this config

## <a name="service"></a>2. Property `QWC Permalink Service > service`

**Title:** Service name

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"permalink"`

## <a name="config"></a>3. Property `QWC Permalink Service > config`

**Title:** Config options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description                                     |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------------- |
| + [db_url](#config_db_url )                             | No      | string | No         | -          | DB connection URL                                     |
| + [permalinks_table](#config_permalinks_table )         | No      | string | No         | -          | Permalink table                                       |
| - [user_permalink_table](#config_user_permalink_table ) | No      | string | No         | -          | User permalink table                                  |
| - [bookmarks_sort_order](#config_bookmarks_sort_order ) | No      | string | No         | -          | Bookmarks sort order, defaults to "date, description" |

### <a name="config_db_url"></a>3.1. Property `QWC Permalink Service > config > db_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** DB connection URL

### <a name="config_permalinks_table"></a>3.2. Property `QWC Permalink Service > config > permalinks_table`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Permalink table

### <a name="config_user_permalink_table"></a>3.3. Property `QWC Permalink Service > config > user_permalink_table`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User permalink table

### <a name="config_bookmarks_sort_order"></a>3.4. Property `QWC Permalink Service > config > bookmarks_sort_order`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Bookmarks sort order, defaults to "date, description"

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2023-03-31 at 10:25:42 +0200
