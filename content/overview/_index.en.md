+++
title = "Overview"
date = 2021-09-17T15:56:40+02:00
weight = 1
chapter = false
+++

The QWC Services are a collection of microservices providing configurations for and authorized access to different QWC Map Viewer components.

![qwc-services-arch](/images/qwc-services-arch.png)

A QWC services SDI has the following main components:
- **Auth-Service**: Authentication service. Currently supported: User DB, LDAP/AD, SAML or Kerberos.
- **Map Viewer**: QWC2 Webclient with configered tools, open and protected maps.
- **OGC Service**: Frontend with access control for WMS and WFS.
- **REST Services**: Services providing an API for Search, Mapinfo, etc.
- **QGIS Server**: Server for map rendering (WMS) and WFS publication.
- **Solr**: Apache Solr fulltext search engine. Backend for geodata and metadata search.
- **Reporting Server**: Jasper Reporting server.
- **Admin GUI**: Administration UI for managing users, permissions, etc.

### User- and access control managment

For authentication the following services are currently provided:

  - qwc-db-auth: Integrated User-DB
  - qwc-ldap-auth: LDAP / Active Directory
  - qwc-saml-auth: SAML 2.0
  - qwc-kerberos-auth: Kerberos

The config/user DB is used in all authentication methods for managing permissions.

After successful identification, all authentcation services issue a JWT 
token which is forwarded to other services either as session cookie or via
HTTP header.
The JWT token contains username and roles of the authenticated user. Services 
requring authentication use a common library for reading the JWT content
and checking the cryptographic signature.

Authorization is managed by each service. Services like QGIS server, which
don't have built-in permission control, are  protected by frontend services
like "«qwc-ogc-service".

**Groups and roles**

Different permissions (e.g. read or write) for accessing resources can
be granted to "roles". Roles are associated with users or user groups.
A user can be member of multiple groups and can also have multiple direct roles.

![](/images/100002010000019100000075E735E86EF7DB022F.png)

If an authentication service returns group information from an IDP, group
permissions can be directly used, without registering individual users.

### REST API

qwc-services communinicate via REST APIs, which are documented according to 
the OpenAPI specification.

![Illustration 2: OpenAPI Dokumentation Data
Service](/images/swagger.jpg)

### Search

Apache Solr (<https://solr.apache.org/>) is used as integrated search engine.
The fulltext search engine with faceted search capabilities is available
with an Apache license and is used by internet search engines like
DuckDuckGo.

Search categories ("facets") can be configured as globally available for
maps or dependent on active layers only. An assigned "filterword" can be
used as shortcut for limiting searches on a category.

![](/images/search.png)

Grouping and sorting of search results is dependent on the result count
per category. If many results are available, an additional section
for search refining is showed in the results. There is also a history
of recent searches.

### Information query

Map info queries are handled by the qwc-feature-info-service providing
an WMS GetFeatureInfo API.

The following info query types can be configured for each layer::

  - WMS feature info query (default): Forwarded to QGIS Server
  - DB Query: Execution of a user-defined SQL query
  - Custom Info module: Specific Python module for returning layer information

Result data of the query module is rendered with the Jinja template engine (with
customizable HTML templates) and returned to the web client as GetFeatureInfoResponse.

![](/images/feature-info.png)

### Measuring tools

Tools for position, distance, area and heading measurements are provided. Units are
user selecteable.

The qwc-elevation-service returns height profiles for distance measurements. The 
mouse position in the height profile is marked in the map and shows a distance
height measurement.

![](/images/measure.png).

### Printing

Printing layouts included in QGIS projects can be used for printing.
Users can select permitted layouts in the print dialog. System provided information
like print date, scale bar, coordinate systems, north arraw and scale can
be used in the priint layout.

User editable text fields like map title or remarks can be provided as well.
