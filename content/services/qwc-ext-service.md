+++
title = "qwc-ext-service"
weight = 12
+++

QWC external link service
=========================

API documentation:

    http://localhost:5023/api/


Setup
-----

Declare the resource type in the config database:

    INSERT INTO qwc_config.resource_types(name, description, list_order) values ('external_links', 'External link name', <list_order>);

Pick `<list_order>` according to the desired ordering position in the resource selection menu in the QWC Admin GUI.

Configuration
-------------

The static config files are stored as JSON files in `$CONFIG_PATH` with subdirectories for each tenant,
e.g. `$CONFIG_PATH/default/*.json`. The default tenant name is `default`.

### JSON config

* [JSON schema](schemas/qwc-ext-service.json)
* File location: `$CONFIG_PATH/<tenant>/extConfig.json`

Example:
```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-ext-service/master/schemas/qwc-ext-service.json",
  "service": "ext",
  "config": {
    "program_map": {
      "prog1": "http://my.secret.site/path/?tenant=$tenant$",
    }
  },
  "resources": {
    "external_program_names": [
      "prog1"
    ]
  }
}
```

Development
-----------

Create a virtual environment:

    virtualenv --python=/usr/bin/python3 .venv

Activate virtual environment:

    source .venv/bin/activate

Install requirements:

    pip install -r requirements.txt

Set the `CONFIG_PATH` environment variable to the path containing the service config and permission files when starting this service (default: `config`).

    export CONFIG_PATH=../qwc-docker/demo-config

Configure environment:

    echo FLASK_ENV=development >.flaskenv

Start local service:

    python server.py
