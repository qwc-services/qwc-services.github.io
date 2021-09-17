all:

fetch:
	no=1; \
	for repo in qwc-map-viewer qwc-ogc-service qwc-feature-info-service qwc-fulltext-search-service qwc-legend-service qwc-permalink-service qwc-print-service  qwc-mapinfo-service qwc-data-service qwc-document-service qwc-elevation-service qwc-ext-service qwc-admin-gui qwc-registration-gui qwc-config-generator; do \
		echo "+++\ntitle = \"$$repo\"\nweight = $$no\n+++" >content/services/$$repo.md; \
		curl -s -L https://github.com/qwc-services/$$repo/raw/master/README.md | sed '/^\[/d' >>content/services/$$repo.md; \
		no=$$((no+1)); \
	done
	no=1; \
	for repo in qwc-db-auth qwc-ldap-auth; do \
		echo "+++\ntitle = \"$$repo\"\nweight = $$no\n+++" >content/authentication/$$repo.md; \
		curl -s -L https://github.com/qwc-services/$$repo/raw/master/README.md | sed '/^\[/d' >>content/authentication/$$repo.md; \
		no=$$((no+1)); \
	done
	echo "+++\ntitle = \"Viewer\"\nweight = 3\n+++\n" >content/viewer/_index.md; \
	curl -s -L https://github.com/qgis/qwc2-demo-app/raw/master/doc/QWC2_Documentation.md >>content/viewer/_index.md;
