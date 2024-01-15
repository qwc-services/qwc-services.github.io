#!/bin/bash

branch=$(git branch --show-current)

echo "* Setting up venv..."
rm -rf .venv
python3 -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt

if [ "$1" == "--update" ] || [ ! -f qwc2.yml ]; then
echo "# References" > src/references/index.md
echo "" >> src/references/index.md

echo "* Getting latest version..."
version=$(curl https://raw.githubusercontent.com/qgis/qwc2-demo-app/${branch}/package.json | grep -Eo '^\s*"version": "[^"]+",$' | awk -F'"' '{print $4}')
sed "s|@version@|$version|" qwc2.yml.in > qwc2.yml

echo "* Downloading plugin reference..."
wget -q -O src/references/qwc2_plugins.md https://raw.githubusercontent.com/qgis/qwc2/${branch}/doc/plugins.md
echo "* [QWC2 plugins](qwc2_plugins.md)" >> src/references/index.md

mkdir -p tmp
echo "* Downloading schema versions..."
wget -q -O tmp/schema-versions.json https://github.com/qwc-services/qwc-config-generator/raw/${branch}/schemas/schema-versions.json

for schemaUrl in \
    https://github.com/qwc-services/qwc-config-generator/raw/${branch}/schemas/qwc-config-generator.json \
    $(cat tmp/schema-versions.json | grep schema_url | awk -F'"' '{print $4}');
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
mike deploy -F qwc2.yml $master

# cleanup venv
echo "* Clean venv..."
deactivate
rm -rf .venv
