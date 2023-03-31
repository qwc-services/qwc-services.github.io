+++
menuTitle = "qwc-elevation-service"
weight = 10
+++
# QWC Elevation Service

- [1. Property `QWC Elevation Service > $schema`](#$schema)
- [2. Property `QWC Elevation Service > service`](#service)
- [3. Property `QWC Elevation Service > config`](#config)
  - [3.1. Property `QWC Elevation Service > config > elevation_dataset`](#config_elevation_dataset)

**Title:** QWC Elevation Service

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

## <a name="$schema"></a>1. Property `QWC Elevation Service > $schema`

**Title:** JSON Schema

|              |                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Type**     | `string`                                                                                                           |
| **Required** | No                                                                                                                 |
| **Format**   | `uri`                                                                                                              |
| **Default**  | `"https://raw.githubusercontent.com/qwc-services/qwc-elevation-service/master/schemas/qwc-elevation-service.json"` |

**Description:** Reference to JSON schema of this config

## <a name="service"></a>2. Property `QWC Elevation Service > service`

**Title:** Service name

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"elevation"`

## <a name="config"></a>3. Property `QWC Elevation Service > config`

**Title:** Config options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                          | Pattern | Type   | Deprecated | Definition | Title/Description                                                                       |
| ------------------------------------------------- | ------- | ------ | ---------- | ---------- | --------------------------------------------------------------------------------------- |
| + [elevation_dataset](#config_elevation_dataset ) | No      | string | No         | -          | Elevation dataset (file or URL). Example: https://data.sourcepole.com/srtm_1km_3857.tif |

### <a name="config_elevation_dataset"></a>3.1. Property `QWC Elevation Service > config > elevation_dataset`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Elevation dataset (file or URL). Example: https://data.sourcepole.com/srtm_1km_3857.tif

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2023-03-31 at 10:25:49 +0200
