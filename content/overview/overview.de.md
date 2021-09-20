+++
title = "Übersicht"
date = 2021-09-17T15:56:40+02:00
weight = 1
chapter = false
+++

The QWC Services are a collection of microservices providing configurations for and authorized access to different QWC Map Viewer components.

![qwc-services-arch](/images/qwc-services-arch.png)

Die GDI besteht aus folgenden Server-Komponenten:
- **Auth-Service**: Es werden verschiedene Authentisierungs-Methoden unterstützt. Z.B. HTTP Basic Authentication mit User-DB, AD/LDAP, SAML und Kerberos.
  Die direkt zugänglichen Dienste enthalten eine Autorisierungsschicht für alle Zugriffe. 
- **Map Viewer**: QWC2 Webclient mit konfigurierten Tools, offenen und zugriffsgeschützten Karten.
- **OGC Service**: Frontend mit Zugriffskontrolle für WMS, WFS und WMTS.
- **REST Services**: API Funktionen wie Search, GetLegend, etc.
- **QGIS Server WMS/WFS**: Server für Kartendienste (WMS) und Datendienste (WFS)
- **Solr**: Apache Solr Search-Engine. Dient als Backend für die Suche von Geodaten und Metadaten.
- **Reporting-Server**: Server-Komponente zur Erzeugung von Reports.
- **Administration**: Adminstrations-GUI für die Verwaltung von Usern, Rechten, Metadaten, etc.

### User- und Zugriffsmanagement

Für die Authentifizierung stehen folgende Services zur Verfügung:

  - qwc-db-auth: Integrierte User-DB
  - qwc-ldap-auth: LDAP / Active Directory
  - qwc-saml-auth: SAML 2.0
  - qwc-kerberos-auth: Kerberos

Die User-DB ist wird bei allen Authentisierungsmethoden benutzt, um
Usern weitergehende Rechte zu vergeben.

Alle Authentisierungsdienste stellen nach erfolgreicher Identifikation
ein JWT-Token aus, welches mit einem Session-Cookie oder via HTTP-Header
an die Dienste weitergeleitet wird. Das JWT-Token enthält den Usernamen
und die Rollen des Users. Die Dienste nutzen eine gemeinsame Bibliothek
zur Verarbeitung des Tokens. Diese stellt sicher, dass die
kryptographische Signatur des Tokens geprüft wird.

Die Authorisierung wird von den einzelnen Diensten sichergestellt. Für
den Dienstserver übernimmt der vorgeschaltete Service «qwc-ogc-service»
die Authorisierung.

**Gruppen und Rollen**

Einem User werden Zugriffsberechtigungen zu Ressourcen zugeordnet, oder
umgekehrt jeder Ressource eine Liste der jeweils zugelassenen Benutzer.

Mit dem Konzept von Benutzergruppen und Rollen lassen sich
Berechtigungen zusammenfassen. User können in Gruppen organisiert
werden. Werden vom Authentisierungsservice Gruppen-Informationen von
einem IDP übernommen, dann können die Gruppenrechte auch ohne Erfassung
der Userinformationen angewandt werden.

Zugriffsrechte, werden in einer Rollendefinition zusammengefasst. Eine
Auflistung von Zugriffsrechten wird häufig auch auch Access Control List
(ACL) genannt.

Diese Rollen (eine oder mehrere) können Usern oder Gruppen zugeordnet werden.

![](/images/100002010000019100000075E735E86EF7DB022F.png)


### REST-API

Die qwc-services werden über ein REST-API angesprochen. Dieses ist in
Form einer OpenAPI-Spezifikation dokumentiert.

![Illustration 2: OpenAPI Dokumentation Data
Service](/images/10000201000006C1000007848FFF3358691E995D.png)

Der config-service, welcher für die Verwaltung der
Service-Konfigurationen und -Permissions zuständig ist, hat ein intern
zugängliches API für den Update einer Konfiguration und
Abfrage-Funktionen. Für dieses Projekt wird das API um weitere
Funktionen zur Anpassung von Konfigurationene erweitert.

### Legende

Der qwc-legend-service unterstützt die Erstellung von Legenden via
Dienstserver oder die Aufbereitung der Legende mit konfigurierten
Bildern. So können dynamische Legenden mit automatisch vom Kartenserver
generierten Legenden, sowie manuell erstellte Legenden kombiniert
werden. 

![](/images/100002010000013F000002C91A6324D14C5FD85E.png)

### Suche

Als Search-Engine wird Apache Solr (<https://solr.apache.org/>)
integriert. Die Volltext Search-Engine mit «Facet»-Suche ist unter der
Apache Lizenz erhältlich und wird unter anderem von
Internetsuchmaschinen wie DuckDuckGo eingesetzt.

Für den Viewer können abhängig vom Thema Suchkategorieren definiert
werden, die immer berücksichtigt werden und einzelnen Layern können
Suchkategrien zugeordnet werden, welche nur bei aktiver Layeranzeige
verwendet werden. Einem Layer kann ein Filterwort zugeordnet werden,
welches zur Kategorieneinschränkung im Viewer verwendet werden kann.

![](/images/search.png)

Die Gruppierung und Sortierung der Resultate erfolgt abhängig von der
Anzahl Treffer innerhalb der Kategorieren. Bei einer grossen Trefferzahl
wird der Abschnitt zur Verfeinerung der Suche aufgeklappt. Es wird eine
History der letzten Suchbegriffen geführt.

### Informationsabfrage

Informationsabfragen werden über den qwc-feature-info-service
abgehandelt. Die Abfrage erfolgt mit dem WMS GetFeatureInfo-API auf eine
geographische Position und bestimmte Layer.

Für jeden Layer kann eine der folgenden Arten zur Informationsabfrage
konfiguriert werden:

  - WMS Geoinformation (Standard): Weiterleitung an QGIS Server
  - DB Query: Ausführung einer konfigurierten DB-Query
  - Custom Info-Modul: Spezifisches Python-Modul zur Rücklieferung der
    Layer-Info

Die Resultate des Abfragemoduls werden mittels eines konfigurierbaren
HTML-Templates gerendert und als GetFeatureInfoResponse an den Webclient
zurückgeliefert.

![](/images/feature-info.png)

Die Darstellung der Ergebnisanzeige wird im Rahmen des Projekts den
Kundenwünschen angepasst (z.B. Löschfunktion).

### Messen

Es stehen Messwerkzeuge für Position, Länge, Fläche und Richtung zur
Verfügung. Masseinheiten sind vom User wählbar.

Der qwc-elevation-service
liefert auf Anfrage ein Höhenprofil zurück, welches bei der
Längenmessung angezeigt werden kann. Die Mausposition im Profil wird in
der Karte markiert und mit Distanzangabe und Höhe
versehen

![](/images/measure.png).

### Drucken

Der Kartendruck erfolgt über vordefinierte Druckvorlagen. Die
Druckvorlagen werden mit QGIS als Layout erstellt und gepflegt. Dabei
ist es möglich sehr hochwertige und flexible Kartenvorlagen zu erstellen
mit einer Auflösung bis zu 1200dpi zu erstellen. Die vordefinierten
Druckvorlagen stehen dem Benutzer über eine Auswahlliste im QWC2 Client
zur Verfügung. Für beliebige Fachkarten können kartenspezifische
Druckvorlagen erstellt werden. Systemgesteuerte Angaben wie Druckdatum,
Massstabsleiste, Referenzkoordinaten, Nordpfeil und Massstabszahl sowie
viele weitere Informationen sind in den Druckvorlagen integrierbar. 

Editierbare Textfelder die durch den Benutzer angepasst werden können
(z.B. Kartentitel, Bemerkungen etc.) sind verfügbar. Die frei
editierbaren Textfelder bleiben beim Wechsel der Druckvorlage (z.B. A4
quer zu A4 hoch) erhalten.

Vor dem Druck kann der Anwender im QWC2-Client den gewünschten
Druckmassstab einstellen. Es werden sowohl eine Massstabsliste als auch
ein frei wählbarer Massstab angeboten.

Nach dem der Ausdruck aufbereitet wurde wird dem Anwender die gewünschte
Karte in gewünschter Auflösung als PDF zum Download angeboten.
