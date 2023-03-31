+++
menuTitle = "qwc-elevation-service"
weight = 11
chapter = false
+++

QWC Elevation Service
=====================

Returns elevations.


Configuration
-------------

The static config files are stored as JSON files in `$CONFIG_PATH` with subdirectories for each tenant,
e.g. `$CONFIG_PATH/default/*.json`. The default tenant name is `default`.

### Elevation Service config

* [JSON schema]({{< ref "setup/schemas/qwc-elevation-service" >}})
* File location: `$CONFIG_PATH/<tenant>/elevationConfig.json`

Example:
```json
{
  "$schema": "https://raw.githubusercontent.com/qwc-services/qwc-elevation-service/master/schemas/qwc-elevation-service.json",
  "service": "elevation",
  "config": {
    "elevation_dataset": "/vsicurl/https://data.sourcepole.com/srtm_1km_3857.tif"
  }
}
```

### Environment variables

Config options in the config file can be overridden by equivalent uppercase environment variables.

| Variable                | Description            |
|-------------------------|------------------------|
| ELEVATION_DATASET       | path/to/dtm.tif        |


Usage
-----

Run as

    python server.py

Requires GDAL Python bindings. `python-gdal` or `python3-gdal` packages on Debian/Ubuntu (Note: virtualenv creation requires --system-site-packages option).

API:
* Runs by default on `http://localhost:5002`
* `GET: /getelevation?pos=<pos>&crs=<crs>`
  - *pos*: the query position, as `x,y`
  - *crs*: the crs of the query position
  - *output*: a json document with the elevation in meters: `{elevation: h}`
* `POST: /getheightprofile`
  - *payload*: a json document as follows:

        {
            coordinates: [[x1,y1],[x2,y2],...],
            distances: [<dist_p1_p2>, <dist_p2_p3>, ...],
            projection: <EPSG:XXXX, projection of coordinates>,
            samples: <number of height samples to return>
        }

  - *output*: a json document with heights in meters: `{elevations: [h1, h2, ...]}`


Docker usage
------------

The docker image can be run with the following command:

    docker run -p 5002:9090 sourcepole/qwc-elevation-service


| docker parameters | Description |
|----------------------|-------------|
|`-p 5002:9090` | Bind port 5002 on the host machine |
