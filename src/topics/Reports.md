# Reports

QWC2, complemented with the [`qwc-document-service`](https://github.com/qwc-services/qwc-document-service/), provides the possibility to generate reports for features of layers whose datasource is a PostgreSQL table, based on [Jasper](https://community.jaspersoft.com/download-jaspersoft/community-edition/) report templates.

## Setting up the document-service
As a first step, set up a [`qwc-document-service`](https://github.com/qwc-services/qwc-document-service/), placing your report templates below the `report_dir`. Read the `qwc-document-service` [`README`](../references/qwc-document-service_readme.md) for more information on setting up the service and to understand how to prepare and configure your report templates.

When using `qwc-docker`, you can configure the container as follows:

```yml
  qwc-document-service:
    image: docker.io/sourcepole/qwc-document-service:<tag>
    environment:
      <<: *qwc-service-variables
      SERVICE_MOUNTPOINT: '/api/v1/document'
      # FLASK_DEBUG: 1
    volumes:
      - ./pg_service.conf:/srv/pg_service.conf:ro
      - ./volumes/reports:/reports
      - ./volumes/reports/fonts:/srv/qwc_service/fonts
      - ./volumes/config:/srv/qwc_service/config:ro
```

In addition, to ensure that the `qwc-config-generator` automatically picks up existing reports when generating the document service configuration, ensure that the reports directory is also mounted in its container:

```yml
  qwc-config-service:
    image: docker.io/sourcepole/qwc-config-generator:<tag>
    ...
    volumes:
      ...
      - ./volumes/reports:/reports
```

## Configuring the web client
As a second step, associate the report templates to theme layers to expose the reports in the web client. This is done providing a `featureReport` entry in a theme item in [`themesConfig.json`](../configuration/ThemesConfiguration.md#manual-theme-configuration) as follows:

```json
    "featureReport": {
      "<layer_name1>": "<template_name1>",
      "<layer_name2>": "<template_name2>",
      ...
    }
```

The web client will then display a link to download the report for one or more selected features in the identify results dialog.

In addition, the [`Reports` plugin](../references/qwc2_plugins.md#reports) provides a convenient interface to directly select a desired report layer and download the reports for one or more, or all, features of the selected layer.

## Example
Here is an example to configure a report for a layer, whose datasource is a PostgreSQL table, assuming a `qwc-docker` setup.

- Create a Jasper report template using [Jasper Studio](https://community.jaspersoft.com/download-jaspersoft/community-edition/) with the desired layout.
  - To include data from the PostgreSQL datasource in your report, add a Postgres Data Adapter, using the name of the PG service definition in your `pg_service.conf` as the name of the data adapter.
  - Create a report parameter, though which the document-service will pass the primary key of report feature.
  - Define the data query in the `Dataset and Query Dialog`,  in the form

        SELECT <fields> FROM <table_name> WHERE <pk_column> = $P{<FEATURE_PARAM_NAME>}

    If you need a more complex query, you'll need to explicitly specify the `table_name`, `pk_column` and `FEATURE_PARAM_NAME` in the document template resource configuration, see below.

  - If you want to include external resources (images, etc), set the resource path relative to the `$P{REPORT_DIR}` path as described in the [`README`](../references/qwc-document-service_readme.md).

- Save your report to the document service report dir, i.e. as `volumes/reports/MyReport.jrxml`.

  - If you included any custom fonts in your report, place these in `ttf` format in `volumes/reports/fonts` respecting the naming convention described in the [`README`](../references/qwc-document-service_readme.md).

- Associate the report with a layer via `themesConfig.json` by adding the following to the desired theme configuration entry:

```json
    "featureReport": {
      "my_layer": "MyReport"
    }
```

- *Note*: `MyReport` here denotes the relative path of `MyReport.jrxml` below `volumes/reports`, without the `.jrxml` extension.

- If the name of the data adapter does not match the name of a PG service definition, or if your report contains a complex data query SQL, from which the dataset table name, primary key column of feature parameter name cannot be trivially parsed, then you need to explicitly define these `document_templates` in the `resources` block of the `document` configuration section in `tenantConfig.json`, for instance:

```json
    {
      "name": "document",
      "config": {...},
      "resources": {
        "document_templates": [
          {
            "template": "MyReport",
            "datasource": "<pg_service_name>",
            "table": "<table_name>",
            "primary_key": "<primary_key_column_name>",
            "parameter_name": "<report_parameter_name>"
          }
        ]
      }
    }
```
- Generate the document service configuration by running the ConfigGenerator. It will automatically pick up all `*.jrxml` files and generate corresponding `document_templates` resources, complementing any manually defined resources.

- To restrict document templates to specified roles, create `Document template` resources and permissions as desired. These permissions will also apply to any reports included as subreports by a parent report.

- Test your report, either through the QWC2 interface, or via a direct call to the document service, i.e.:

      http://localhost:8088/api/v1/document/MyReport.pdf?feature=<fid>

  *Note*: check the logs of the `qwc-document-service` (in particular with `FLASK_DEBUG: 1`) to get detailed information about the report generation.
