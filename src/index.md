# QWC2 / QWC Services

![QWC2](images/qwc2.png?style=centerme)

QGIS Web Client 2 (QWC2) is a modular next generation responsive web client for QGIS Server, built with ReactJS and OpenLayers.

![Overview](images/overview.png?style=centerme)

The core concept of QWC2 is to display QGIS Projects which are published by QGIS Server via WMS.

There are two ways to run QWC2:

- As part of the *qwc-services* ecosystem, includes additional services to which includes additional services to extend the viewer functionality (such as user administration, editing, etc.). This is the recommended approach.
- As a standalone viewer (static JS/HTML/CSS web application) on top of QGIS Server.

QWC2 with qwc-services on the backend provide a complete Web GIS infrastructure.

## Overview of functionalities

Without any additional services, the stock QWC2 offers the following main functionalities:

- Theme switcher (a theme is a published QGIS project)
- Switchable background layers
- Layer tree
- Object information (feature info)
- Search with configurable providers
- Measurement tools
- Redlining (sketching)
- URL sharing
- Geolocation
- PDF printing
- Raster and DXF export
- Compare layers
- Import external layers (WMS, WFS, WMTS, KML, GeoJSON)

When run as part of the qwc-services ecosystem, the following additional viewer functionalities are available:

- User administration
- Editing
- Fulltext search
- Compact permalinks
- Height profile
- Custom feature info templates
- Mapinfo popup
- Reports (via Jasper)

qwc-services also provides the following enterprise relevant functionalities:

* Docker/Kubernetes or WSGI deployments
* Multi-tenant setup
* Custom service integration
* Multiple authentication backends

## Explore

* [Developer Quickstart](QuickStart.md)
* [User guide](UserGuide.md)
* Some public viewers: [QWC2 demo instance](https://qwc2.sourcepole.ch) | [Glarus](https://map.geo.gl.ch/) | [Solothurn](https://geo.so.ch/map/) | [Oslandia](https://qgis.oslandia.net/) | [Erft Verband](http://webgis.erftverband.de)

## Support

* Community support: [Github](https://github.com/qgis/qwc2/issues)
* Commercial Support: [Sourcepole](https://www.sourcepole.com/), [Oslandia](https://oslandia.com/) and other companies.
* [Improve this web site](https://github.com/qwc-services/qwc-services.github.io/)
