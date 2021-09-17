+++
title = "Overview"
date = 2021-09-17T15:56:40+02:00
weight = 1
chapter = false
+++

The QWC Services are a collection of microservices providing configurations for and authorized access to different QWC Map Viewer components.

![qwc-services-arch](/images/qwc-services-arch.png)

# QWC Services

Applications:
* [Map Viewer](https://github.com/qwc-services/qwc-map-viewer)
* [QWC configuration backend](https://github.com/qwc-services/qwc-admin-gui)
* [Registration GUI](https://github.com/qwc-services/qwc-registration-gui)

REST services:
* [Authentication service with local user database](https://github.com/qwc-services/qwc-db-auth)
* [OGC service](https://github.com/qwc-services/qwc-ogc-service)
* [Data service](https://github.com/qwc-services/qwc-data-service)
* [Permalink service](https://github.com/qwc-services/qwc-permalink-service)
* [Elevation service](https://github.com/qwc-services/qwc-elevation-service)
* [Mapinfo service](https://github.com/qwc-services/qwc-mapinfo-service)
* [Document service](https://github.com/qwc-services/qwc-document-service)
* [Print service](https://github.com/qwc-services/qwc-print-service)
* [Fulltext search service](https://github.com/qwc-services/qwc-fulltext-search-service)

Configuration database:
* [DB schema and migrations](https://github.com/qwc-services/qwc-config-db)

Docker:
* [Docker containers for QWC services](https://github.com/qwc-services/qwc-docker)
