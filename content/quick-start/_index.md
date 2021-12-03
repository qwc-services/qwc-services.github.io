+++
title = "Quick Start"
date = 2021-09-17T15:10:55+02:00
weight = 2
chapter = false
+++

### Docker containers for QWC services

Create a QWC services dir:

    mkdir qwc-services
    cd qwc-services/

Clone [Docker containers for QWC services](https://github.com/qwc-services/qwc-docker):

    git clone https://github.com/qwc-services/qwc-docker.git

Install Docker and setup containers (see [qwc-docker README](https://github.com/qwc-services/qwc-docker#setup)):

    cd qwc-docker/
    cp docker-compose-example.yml docker-compose.yml

Create a secret key:

    python3 -c 'import secrets; print("JWT_SECRET_KEY=\"%s\"" % secrets.token_hex(48))' >.env

Set permissions for writable volumes:

    sudo chown -R www-data:www-data volumes/qgs-resources
    sudo chown -R www-data:www-data volumes/config
    sudo chown -R www-data:www-data volumes/qwc2/assets

    sudo chown 8983:8983 volumes/solr/data

### Run containers

Start all containers:

    docker-compose up -d

Follow log output:

    docker-compose logs -f

Open map viewer:

    http://localhost:8088/

Open Admin GUI (Admin user: `admin:admin`, requires password change on first login):

    http://localhost:8088/qwc_admin

Sign in (Demo user: `demo:demo`):

    http://localhost:8088/auth/login

Sign out:

    http://localhost:8088/auth/logout

Stop all containers:

    docker-compose down

### Add a QGIS project

Setup PostgreSQL connection service file `~/.pg_service.conf`
for DB connections from the host machine to PostGIS container:

```
cat >>~/.pg_service.conf <<EOS
[qwc_geodb]
host=localhost
port=5439
dbname=qwc_demo
user=qwc_service
password=qwc_service
sslmode=disable
EOS
```

* Open project `demo-projects/natural-earth-countries.qgz` with QGIS and save as `volumes/config-in/default/qgis_projects/natural-earth-countries.qgs`
* Update configuration in Admin GUI

### Add an editable layer

* Add `edit_polygon` layer in QGIS project
* Add map and data resources with permissions
* Update configuration in Admin GUI

### Add a custom edit form

Adapt edit form with Drag and Drop Designer:
* Change attribute form type to `Drag and Drop Designer`.
* Change form layout
* Update configuration in Admin GUI

Use the previously generated edit form in `volumes/qwc2/assets/forms/autogen/` as a template.

Edit and save the form with QT Designer.

Copy the form into the volumes:

    sudo cp natural-earth-countries_edit_polygons.ui volumes/config-in/default/qgis_projects/
    sudo cp natural-earth-countries_edit_polygons.ui volumes/qgs-resources/

Change attribute form type to `Provide ui-file`.

Select `natural-earth-countries_edit_polygons.ui` as `Edit UI`.

Update configuration in Admin GUI.

### Enable Fulltext search

Make solr owner of solr data
    sudo chown 8983:8983 volumes/solr/data

    # Cleanup
    sudo rm -rf volumes/solr/data/*

    docker-compose restart qwc-solr

    curl 'http://localhost:8983/solr/gdi/dih_geodata?command=full-import'
    curl 'http://localhost:8983/solr/gdi/dih_geodata?command=status'
    curl 'http://localhost:8983/solr/gdi/select?q=search_1_stem:austr*'

    curl 'http://localhost:8983/solr/gdi/dih_metadata?command=full-import&clean=false'
    curl 'http://localhost:8983/solr/gdi/dih_metadata?command=status'
    curl 'http://localhost:8983/solr/gdi/select?q=search_1_stem:qwc_demo'

Test query for fulltext search:

    curl 'http://localhost:8983/solr/gdi/select?q=search_1_stem:austr*'
