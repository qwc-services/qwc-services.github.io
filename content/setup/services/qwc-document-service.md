+++
menuTitle = "qwc-document-service"
weight = 10
chapter = false
+++

Document service
================

The document service delivers reports from the Jasper reporting service with permission control.


Dependencies
------------

* [Jasper reporting service](https://github.com/qwc-services/jasper-reporting-service/)


Configuration
-------------

The static config files are stored as JSON files in `$CONFIG_PATH` with subdirectories for each tenant,
e.g. `$CONFIG_PATH/default/*.json`. The default tenant name is `default`.

### JSON config

* [JSON schema](schemas/qwc-document-service.json)
* File location: `$CONFIG_PATH/<tenant>/documentConfig.json`

Example:
```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-document-service/master/schemas/qwc-document-service.json",
  "service": "document",
  "config": {
    "jasper_service_url": "http://localhost:8002/reports",
    "jasper_timeout": 60
  },
  "resources": {
    "document_templates": [
      {
        "template": "demo",
        "report_filename": "PieChartReport"
      }
    ]
  }
}
```

### Environment variables

Config options in the config file can be overridden by equivalent uppercase environment variables.

Environment variables:

| Variable             | Description                | Default value                 |
|----------------------|----------------------------|-------------------------------|
| `JASPER_SERVICE_URL` | Jasper Reports service URL | http://localhost:8002/reports |
| `JASPER_TIMEOUT`     | Timeout (s)                | 60                            |


Usage
-----

API documentation:

    http://localhost:5018/api/

Request format:

    http://localhost:5018/<template>?<key>=<value>&...

Example:

    http://localhost:5018/BelasteteStandorte.pdf

Arbitrary parameters can be appended to the request:

    http://localhost:5018/BelasteteStandorte.pdf?feature=123

The format of the report is extracted from the template name, i.e.

    http://localhost:5018/BelasteteStandorte.xls?feature=123

If no extension is present in the template name, PDF is used as format.

See also jasper-reporting-service README.

Docker usage
------------

To run this docker image you will need a running jasper reporting service.

The following steps explain how to download a jasper reporting service docker image and how to run the `qwc-document-service` with `docker-compose`.

**Step 1: Clone qwc-docker**

    git clone https://github.com/qwc-services/qwc-docker
    cd qwc-docker

**Step 2: Create docker-compose.yml file**

    cp docker-compose-example.yml docker-compose.yml

**Step 3: Start docker containers**

    docker-compose up qwc-document-service

For more information please visit: https://github.com/qwc-services/qwc-docker

Development
-----------

Create a virtual environment:

    virtualenv --python=/usr/bin/python3 .venv

Activate virtual environment:

    source .venv/bin/activate

Install requirements:

    pip install -r requirements.txt

Start local service:

    CONFIG_PATH=/PATH/TO/CONFIGS/ python server.py


Testing
-------

Run all tests:

    python test.py
