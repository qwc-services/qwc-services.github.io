+++
title = "QWC Fulltext Search Service"
menuTitle = "qwc-fulltext-search-service"
weight = 4
+++


Faceted fulltext search and geometry retrieval for search results.


Dependencies
------------

* Solr search service


Configuration
-------------

The static config and permission files are stored as JSON files in `$CONFIG_PATH` with subdirectories for each tenant,
e.g. `$CONFIG_PATH/default/*.json`. The default tenant name is `default`.

### Search Service config

* [JSON schema](schemas/qwc-search-service.json)
* File location: `$CONFIG_PATH/<tenant>/searchConfig.json`

Example:
```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-fulltext-search-service/master/schemas/qwc-search-service.json",
  "service": "search",
  "config": {
    "solr_service_url": "http://localhost:8983/solr/gdi/select",
    "word_split_re": "[\\s,.:;\"]+",
    "search_result_limit": 50,
    "db_url": "postgresql:///?service=qwc_geodb"
  },
  "resources": {
    "facets": [
      {
        "name": "background",
        "filter_word": "Background"
      },
      {
        "name": "foreground",
        "filter_word": "Map"
      },
      {
        "name": "ne_10m_admin_0_countries",
        "filter_word": "Country",
        "table_name": "qwc_geodb.search_v",
        "geometry_column": "geom",
        "facet_column": "subclass"
      }
    ]
  }
}
```

### Permissions

* [JSON schema](https://github.com/qwc-services/qwc-services-core/blob/master/schemas/qwc-services-permissions.json)
* File location: `$CONFIG_PATH/<tenant>/permissions.json`

Example:
```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-services-core/master/schemas/qwc-services-permissions.json",
  "users": [
    {
      "name": "demo",
      "groups": ["demo"],
      "roles": []
    }
  ],
  "groups": [
    {
      "name": "demo",
      "roles": ["demo"]
    }
  ],
  "roles": [
    {
      "role": "public",
      "permissions": {
        "dataproducts": [
          "qwc_demo"
        ],
        "solr_facets": [
          "foreground",
          "ne_10m_admin_0_countries"
        ]
      }
    },
    {
      "role": "demo",
      "permissions": {
        "dataproducts": [],
        "solr_facets": []
      }
    }
  ]
}
```

### Environment variables

Config options in the config file can be overridden by equivalent uppercase environment variables.

| Variable                | Description                                 | Default value                           |
|-------------------------|---------------------------------------------|-----------------------------------------|
| SOLR_SERVICE_URL        | SOLR service URL                            | `http://localhost:8983/solr/gdi/select` |
| WORD_SPLIT_RE           | Word split Regex                            | `[\s,.:;"]+`                            |
| SEARCH_RESULT_LIMIT     | Result count limit per search               | `50`                                    |
| DB_URL                  | DB connection for search geometries view    |                                         |


Solr Setup
----------

Solr Administration User Interface: http://localhost:8983/solr/

Core overview: http://localhost:8983/solr/#/gdi/core-overview

Solr Ref guide: https://lucene.apache.org/solr/guide/8_0/
Indexing: https://lucene.apache.org/solr/guide/8_0/uploading-structured-data-store-data-with-the-data-import-handler.html#dataimporthandler-commands

`solr-precreate` creates core in `/var/solr/data/gdi`.
After a configuration change remove the content of `/var/solr/data`
e.g. with `sudo rm -rf volumes/solr/data/*`

    curl 'http://localhost:8983/solr/gdi/dih_geodata?command=full-import'
    curl 'http://localhost:8983/solr/gdi/dih_geodata?command=status'
    curl 'http://localhost:8983/solr/gdi/select?q=search_1_stem:austr*'

    curl 'http://localhost:8983/solr/gdi/dih_metadata?command=full-import&clean=false'
    curl 'http://localhost:8983/solr/gdi/dih_metadata?command=status'
    curl 'http://localhost:8983/solr/gdi/select?q=search_1_stem:qwc_demo'

If you encounter permission problems with the solr service then try the following commnad:

    chown 8983:8983 volumes/solr/data

Usage/Development
-----------------

Set the `CONFIG_PATH` environment variable to the path containing the service config and permission files when starting this service (default: `config`).

    export CONFIG_PATH=../qwc-docker/demo-config

Overide configurations, if necessary:

    export SOLR_SERVICE_URL=http://localhost:8983/solr/gdi/select

Configure environment:

    echo FLASK_ENV=development >.flaskenv

Start service:

    python server.py

Search base URL:

    http://localhost:5011/

Search API:

    http://localhost:5011/api/

Examples:

    curl 'http://localhost:5011/fts/?filter=foreground,ne_10m_admin_0_countries&searchtext=austr'
    curl 'http://localhost:5011/fts/?filter=foreground,ne_10m_admin_0_countries&searchtext=qwc'

    curl -g 'http://localhost:5011/geom/ne_10m_admin_0_countries/?filter=[["ogc_fid","=",90]]'


Docker usage
------------

To run this docker image you will need a running Solr search service.

The following steps explain how to download the Solr search service docker image and how to run the `qwc-data-service` with `docker-compose`.

**Step 1: Clone qwc-docker**

    git clone https://github.com/qwc-services/qwc-docker
    cd qwc-docker

**Step 2: Create docker-compose.yml file**

    cp docker-compose-example.yml docker-compose.yml

**Step 3: Start docker containers**

    docker-compose up qwc-fulltext-search-service

For more information please visit: https://github.com/qwc-services/qwc-docker


Testing
-------

Run all tests:

    python test.py
