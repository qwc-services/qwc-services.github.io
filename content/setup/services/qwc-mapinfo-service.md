+++
menuTitle = "qwc-mapinfo-service"
weight = 8
chapter = false
+++

QWC MapInfo Service
===================

Additional information at a geographic position displayed with right mouse click on map.


Configuration
-------------

The static config files are stored as JSON files in `$CONFIG_PATH` with subdirectories for each tenant,
e.g. `$CONFIG_PATH/default/*.json`. The default tenant name is `default`.

### MapInfo Service config

* [JSON schema](schemas/qwc-mapinfo-service.json)
* File location: `$CONFIG_PATH/<tenant>/mapinfoConfig.json`

Examples:

```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-mapinfo-service/master/schemas/qwc-mapinfo-service.json",
  "service": "mapinfo",
  "config": {
    "db_url": "postgresql:///?service=qwc_geodb",
    "info_table": "qwc_geodb.ne_10m_admin_0_countries",
    "info_geom_col": "wkb_geometry",
    "info_display_col": "name",
    "info_title": "Country"
  }
}
```

```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-mapinfo-service/master/schemas/qwc-mapinfo-service.json",
  "service": "mapinfo",
  "config": {
    "db_url": "postgresql:///?service=qwc_geodb",
    "info_table": "qwc_geodb.ne_10m_admin_0_countries",
    "info_geom_col": "wkb_geometry",
    "info_display_col": "name",
    "info_title": "Country",
    "info_where": "pop_est > 600000"
  }
}
```

```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-mapinfo-service/master/schemas/qwc-mapinfo-service.json",
  "service": "mapinfo",
  "config": {
    "queries": [
      {
        "db_url": "postgresql:///?service=qwc_geodb",
        "info_table": "qwc_geodb.ne_10m_admin_0_countries",
        "info_geom_col": "wkb_geometry",
        "info_display_col": "name",
        "info_title": "Country"
      },
      {
        "db_url": "postgresql:///?service=qwc_geodb",
        "info_sql": "SELECT type FROM qwc_geodb.ne_10m_admin_0_countries WHERE ST_contains(wkb_geometry, ST_SetSRID(ST_Point(:x, :y), :srid)) LIMIT 1",
        "info_title": "Type"
      }
    ]
  }
}
```


### Environment variables

Config options in the config file can be overridden by equivalent uppercase environment variables.

| Variable            | Description                  |
|---------------------|------------------------------|
| `INFO_TABLE`        | Table to use                 |
| `INFO_GEOM_COL`     | Geometry column in table     |
| `INFO_DISPLAY_COL`  | Display text column in table |
| `INFO_TITLE`        | Display title                |


Usage
-----

Run as

    python server.py

API documentation:

    http://localhost:5016/api/

Docker usage
------------

To run this docker image you will need a PostGIS database. For testing purposes you can use the demo DB.

The following steps explain how to download the demo DB docker image and how to run the `qwc-mapinfo-service` service with `docker-compose`.

**Step 1: Clone qwc-docker**

    git clone https://github.com/qwc-services/qwc-docker
    cd qwc-docker

**Step 2: Create docker-compose.yml file**

    cp docker-compose-example.yml docker-compose.yml

**Step 3: Start docker containers**

    docker-compose up qwc-mapinfo-service

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
