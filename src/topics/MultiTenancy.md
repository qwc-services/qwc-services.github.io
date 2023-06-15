# Multi-Tenancy

Multi-tenancy allows serving multiple viewer configurations from a single installation. Specifically, it allows separate theme, viewer (plugins, appearance, etc.) and user/permissions configurations for each tenant.

By default, `qwc-docker` includes a single `default` tenant, with the respective configuration file located at `qwc-docker/volumes/config-in/default/tenantConfig.json`.

To configure additional tenants, the main steps are as follows:

* Define how the tenant name is extracted from the requests.
* Write a `tenantConfig.json`, specifying the location of the configuration database, the viewer configuration and viewer assets.

## Extracting the tenant name from the requests

Multi-tenancy works by extracting a tenant name from the request URL and passing it to the respective QWC services. A typical setup is to run the application at the base address

    https://<hostname>/<tenant>/

The simplest approach is to extract the tenant name in a rewrite rule and set a corresponding header which will be read by the QWC services. This can be accomplished as follows:

1. Define the name of the tenant header in `qwc-docker/docker-compose.yml` by setting the `TENANT_HEADER` environment variable in the `qwc-service-variables` block, i.e.:
```yml
x-qwc-service-variables: &qwc-service-variables
  [...]
  TENANT_HEADER: Tenant
```

2. Add rewrite rules to the `api-gateway` configuration file `qwc-docker/api-gateway/nginx.conf`, extracting the tenant name and setting the tenant header. For example

```
    location ~ ^/(?<t>tenant1|tenant2|tenant3)/ {
        proxy_set_header Tenant $t;
        rewrite ^/[^/]+(.+) $1 break;
        proxy_pass http://qwc-map-viewer:9090;
    }
    location ~ ^/(?<t>tenant1|tenant2|tenant3)/auth {
        proxy_set_header Tenant $t;
        rewrite ^/[^/]+(.+) $1 break;
        proxy_pass http://qwc-auth-service:9090;
    }
    location ~ ^/(?<t>tenant1|tenant2|tenant3)/admin {
        proxy_set_header Tenant $t;
        rewrite ^/[^/]+(.+) $1 break;
        proxy_pass http://qwc-admin-gui:9090;
    }
    location ~ ^/(?<t>tenant1|tenant2|tenant3)/ows {
        proxy_set_header Tenant $t;
        rewrite ^/[^/]+(.+) $1 break;
        proxy_pass http://qwc-ogc-service:9090;
    }
    location ~ ^/(?<t>tenant1|tenant2|tenant3)/api/v1/featureinfo {
        proxy_set_header Tenant $t;
        rewrite ^/[^/]+(.+) $1 break;
        proxy_pass http://qwc-feature-info-service:9090;
    }
    # etc...
```

## Writing the `tenantConfig.json`

The tenant configuration file `tenantConfig.json` is located at `qwc-docker/volumes/config-in/<tenant>/tenantConfig.json` with `<tenant>` the name of the tenant. There are a number of configuration options which specifically affect the type of multi-tenancy setup, which is very flexible. Possible choices are:

* Shared vs. separate configuration database / admin backend
* Shared vs. separate viewer build
* Shared vs. separate qgs-resources tree
* etc...

In general, you need to ensure that

* All the service URLs point to locations which are handled by the api-gateway configuration.
* All the paths refers to locations which are mounted in `qwc-docker/docker-compose.yml`.
* All database connection service names refer to connections which are defined `qwc-docker/pg_service.conf`.

A minimal configuration for tenant `tenant_name` may look as follows:

```json
{
  "$schema": "https://github.com/qwc-services/qwc-config-generator/raw/master/schemas/qwc-config-generator.json",
  "service": "config-generator",
  "config": {
    "tenant": "tenant_name",
    "default_qgis_server_url": "http://qwc-qgis-server/ows/",
    "config_db_url": "postgresql:///?service=qwc_configdb",
    "qgis_projects_base_dir": "/data",
    "qwc2_base_dir": "/qwc2",
    "ows_prefix": "/tenant_name/ows",
    ...
  },
  "themesConfig": "./themesConfig.json",
  "services": [
    {
      "name": "adminGui",
      "config": {
        "db_url": "postgresql:///?service=qwc_configdb"
      }
    },
    {
      "name": "dbAuth",
      "config": {
        "db_url": "postgresql:///?service=qwc_configdb",
        "config_generator_service_url": "http://qwc-config-service:9090"
      }
    },
    {
      "name": "mapViewer",
      "generator_config": {
        "qwc2_config": {
          "qwc2_config_file": "/srv/qwc_service/config-in/tenant_name/config.json",
          "qwc2_index_file": "/srv/qwc_service/config-in/tenant_name/index.html"
        }
      },
      "config": {
        "qwc2_path": "/qwc2/",
        "auth_service_url": "/tenant_name/auth/",
        "ogc_service_url": "/tenant_name/ows/",
        "info_service_url": "/tenant_name/api/v1/featureinfo/",
        ...
      }
    }
  ]
}
```

*Notes*:

* The database URL (`postgresql:///?service=qwc_configdb`) will determine whether a shared or sperate configuration database is used for each tenant.
* The `qwc2_config_file`, `qwc2_index_file`, `qwc2_base_dir` and `qwc2_path` paths will determine whether the viewer build/configuration is shared or separate for each tenant.
* The various service URLs in the `mapViewer` configuration and in other service configurations need to match what is expected in the `api-gateway` configuration.

## `tenantConfig` template

In particular when managing a large number of tenants, it can be tedious and error-prone to manage separate `tenantConfig.json` files for each tenant which might be nearly identical aside from the tenant name. To alleviate this, you can create a `tenantConfig` template, using the `$tenant$` placeholder where appropriate, and point to this file in the respective `tenantConfig.json` files. The contents of the template will then be merged with the contents of `tenantConfig.json`, and occurence of `$tenant$` in the template will be replaced with the current tenant name.

For example, a minimal `tenantConfig.json` in `qwc-docker/volumes/config-in/tenant_name/` could look as follows:

```json
{
  "$schema": "https://github.com/qwc-services/qwc-config-generator/raw/master/schemas/qwc-config-generator.json",
  "service": "config-generator",
  "template": "../tenantConfig.template.json",
  "config": {
    "tenant": "tenant_name"
  },
  "themesConfig": "./themesConfig.json"
}
```

And the `tenantConfig.template.json` in `qwc-docker/volumes/config-in/` as follows:

```json
{
  "config": {
    "ows_prefix": "$tenant$/ows",
    ...
  },
  "services": [
    {
      "name": "mapViewer",
      "generator_config": {
        "qwc2_config": {
          "qwc2_config_file": "/srv/qwc_service/config-in/$tenant$/config.json",
          "qwc2_index_file": "/srv/qwc_service/config-in/$tenant$/index.html"
        }
      },
      "config": {
        "auth_service_url": "$tenant$/auth/",
        "ogc_service_url": "/$tenant$/ows/",
        "info_service_url": "/$tenant$/api/v1/featureinfo/",
        ...
      }
    },
    ...
  ]
}
```
