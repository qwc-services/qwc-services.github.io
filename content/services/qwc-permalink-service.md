+++
title = "QWC Permalink Service"
menuTitle = "qwc-permalink-service"
weight = 6
+++


Stores and resolves compact permalinks for the Web Client.

Permalinks are stored in a database table.

Configuration
-------------

The static config files are stored as JSON files in `$CONFIG_PATH` with subdirectories for each tenant,
e.g. `$CONFIG_PATH/default/*.json`. The default tenant name is `default`.

### JSON config

* [JSON schema](schemas/qwc-permalink-service.json)
* File location: `$CONFIG_PATH/<tenant>/permalinkConfig.json`

Example:
```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-permalink-service/master/schemas/qwc-permalink-service.json",
  "service": "permalink",
  "config": {
    "db_url": "postgresql:///?service=qwc_configdb",
    "permalinks_table": "qwc_config.permalinks",
    "user_permalink_table": "qwc_config.user_permalinks"
  }
}
```

### Environment variables

Config options in the config file can be overridden by equivalent uppercase environment variables.

| Variable               | Default value                         | Description           |
|------------------------|---------------------------------------|-----------------------|
| `DB_URL`               | `postgresql:///?service=qwc_configdb` | DB connection URL [1] |
| `PERMALINKS_TABLE`     | `qwc_config.permalinks`               | Permalink table       |
| `USER_PERMALINK_TABLE` | `qwc_config.user_permalinks`          | User permalink table  |


If you don't use `qwc-config-db` you have to create the tables for storing permalinks first.
Example:

    CREATE TABLE permalinks
    (
      key character(10) NOT NULL PRIMARY KEY,
      data text,
      date date
    );


Usage
-----

Base URL:

    http://localhost:5018/

API documentation:

    http://localhost:5018/api/


Docker usage
------------

To run this docker image you will need a configuration database. For testing purposes you can use the demo DB.

The following steps explain how to download the demo DB docker image and how to run the `qwc-permalink-service` with `docker-compose`.

**Step 1: Clone qwc-docker**

    git clone https://github.com/qwc-services/qwc-docker
    cd qwc-docker

**Step 2: Create docker-compose.yml file**

    cp docker-compose-example.yml docker-compose.yml

**Step 3: Start docker containers**

    docker-compose up qwc-permalink-service

For more information please visit: https://github.com/qwc-services/qwc-docker

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
