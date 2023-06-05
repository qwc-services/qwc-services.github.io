#!/bin/sh

echo "* Setting up venv..."
rm -rf .venv
python3 -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt

if [ "$1" == "--update" ]; then
echo "# References" > src/references/index.md
echo "" >> src/references/index.md

echo "* Downloading plugin reference..."
wget -q -O src/references/qwc2_plugins.md https://raw.githubusercontent.com/qgis/qwc2-demo-app/master/doc/src/plugins.md
echo "* [QWC2 plugins](qwc2_plugins.md)" >> src/references/index.md

mkdir -p tmp
echo "* Downloading schema versions..."
wget -q -O tmp/schema-versions-master.json https://github.com/qwc-services/qwc-config-generator/raw/master/schemas/schema-versions-master.json

for schemaUrl in \
    https://github.com/qwc-services/qwc-config-generator/raw/master/schemas/qwc-config-generator.json \
    $(cat tmp/schema-versions-master.json | grep schema_url | awk -F'"' '{print $4}');
do
    service=$(basename ${schemaUrl%.json})
    echo "* Generating service schema reference for $service..."
    echo $schemaUrl
    wget -q -O tmp/$service.json $schemaUrl
    generate-schema-doc tmp/$service.json src/references/$service.md

    echo "* [$service]($service.md)" >> src/references/index.md

done
rm -rf tmp
fi

echo "* Clean previous HTML build..."
rm -rf site

echo "* Building HTML..."
mkdocs build -f qwc2.yml

# cleanup venv
echo "* Clean venv..."
deactivate
rm -rf .venv
