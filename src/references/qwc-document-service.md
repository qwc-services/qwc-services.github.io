# QWC Document Service

## Properties

- **`$schema`** *(string)*: Reference to JSON schema of this config. Default: `https://raw.githubusercontent.com/qwc-services/qwc-document-service/master/schemas/qwc-document-service.json`.
- **`service`** *(string)*
- **`config`** *(object)*
  - **`jasper_service_url`** *(string)*: Jasper Reporting service URL for generating reports. Example: http://localhost:8002/reports.
  - **`jasper_timeout`** *(integer)*: Timeout for requests forwarded to Jasper Reporting service. Default: `60`.
- **`resources`** *(object)*
  - **`document_templates`** *(array)*
    - **Items** *(object)*
      - **`template`** *(string)*
      - **`report_filename`** *(string)*
