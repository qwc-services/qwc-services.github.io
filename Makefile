all:

fetch:
	no=1; \
	for repo in qwc-map-viewer qwc-ogc-service qwc-feature-info-service qwc-fulltext-search-service qwc-legend-service qwc-permalink-service qwc-print-service  qwc-mapinfo-service qwc-data-service qwc-document-service qwc-elevation-service qwc-admin-gui qwc-registration-gui qwc-config-generator; do \
		echo "+++\nmenuTitle = \"$$repo\"\nweight = $$no\nchapter = false\n+++" >content/installation/services/$$repo.md; \
		curl -s -L https://github.com/qwc-services/$$repo/raw/master/README.md | sed '/^\[/d' >>content/installation/services/$$repo.md; \
		no=$$((no+1)); \
	done
	no=1; \
	for repo in qwc-db-auth qwc-ldap-auth; do \
		echo "+++\nmenuTitle = \"$$repo\"\nweight = $$no\nchapter = false\n+++" >content/installation/authentication/$$repo.md; \
		curl -s -L https://github.com/qwc-services/$$repo/raw/master/README.md | sed '/^\[/d' >>content/installation/authentication/$$repo.md; \
		no=$$((no+1)); \
	done
	echo "+++\nmenuTitle = \"Viewer\"\nweight = 3\nchapter = false\n+++\n" >content/installation/viewer/_index.md; \
	curl -s -L https://github.com/qgis/qwc2-demo-app/raw/master/doc/QWC2_Documentation.md >>content/installation/viewer/_index.md;

schemas:
	# Convert JSON schemas to Markdown
	# https://github.com/coveooss/json-schema-for-humans
	no=1; \
	for repo in qwc-map-viewer qwc-ogc-service qwc-feature-info-service qwc-fulltext-search-service qwc-legend-service qwc-permalink-service qwc-print-service  qwc-mapinfo-service qwc-data-service qwc-document-service qwc-elevation-service qwc-ext-service qwc-admin-gui qwc-registration-gui qwc-config-generator; do \
		curl -s -o /tmp/schema.json -L https://github.com/qwc-services/$$repo/raw/master/schemas/$$repo.json; \
		echo "+++\ntitle = \"$$repo\"\nweight = $$no\n+++" >content/installation/configuration/$$repo.md; \
		.venv/bin/generate-schema-doc --config template_name=md /tmp/schema.json /tmp/schema.md; \
		cat /tmp/schema.md >>content/installation/configuration/$$repo.md; \
		no=$$((no+1)); \
	done
