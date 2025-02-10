#!/bin/bash

branch=$(git branch --show-current)
branch_main="main"
if [[ "$branch" == *-lts ]]; then
    branch_main=$branch
fi

echo "* Setting up venv..."
rm -rf .venv
python3 -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt

if [ "$1" == "--update" ] || [ ! -f qwc2.yml ]; then
echo "# References" > src/references/index.md
echo "" >> src/references/index.md
echo "index.md" > src/references/.gitignore

echo "* Getting latest version..."
version=$(curl https://raw.githubusercontent.com/qgis/qwc2-demo-app/${branch}/package.json | grep -Eo '^\s*"version": "[^"]+",$' | awk -F'"' '{print $4}')
sed "s|@version@|$version|" qwc2.yml.in > qwc2.yml

echo "* Downloading plugin reference..."
wget -q -O src/references/qwc2_plugins.md https://raw.githubusercontent.com/qgis/qwc2/${branch}/doc/plugins.md
wget -q -O src/references/qwc-base-db_readme.md https://raw.githubusercontent.com/qwc-services/qwc-base-db/${branch_main}/README.md
echo "qwc2_plugins.md" >> src/references/.gitignore
echo "* QWC2 Client" >> src/references/index.md
echo "" >> src/references/index.md
echo "    - [Plugin reference](qwc2_plugins.md)" >> src/references/index.md
echo "" >> src/references/index.md
echo "* qwc-base-db" >> src/references/index.md
echo "" >> src/references/index.md
echo "    - [README](qwc-base-db_readme.md)" >> src/references/index.md
mkdir -p tmp
echo "* Downloading schema versions..."
if [ "$branch" == *-lts ]; then
    wget -q -O tmp/schema-versions.json https://github.com/qwc-services/qwc-config-generator/raw/${branch}/schemas/schema-versions.json
else
    wget -q -O tmp/schema-versions.json https://raw.githubusercontent.com/qwc-services/qwc-config-generator/${branch}/src/schema-versions.json
fi

for schemaUrl in \
    $(cat tmp/schema-versions.json | grep schema_url | awk -F'"' '{print $4}');
do
    service=$(basename ${schemaUrl%.json})
    echo "* Generating service schema reference for $service..."
    echo "  $schemaUrl"
    wget -q -O tmp/$service.json $schemaUrl
    generate-schema-doc tmp/$service.json src/references/$service.md
    echo "$service.md" >> src/references/.gitignore

    readmeUrl=${schemaUrl/schemas\/*.json/README.md}
    echo "* Downloading $service README.md"
    echo "  $readmeUrl"
    wget -q -O src/references/${service}_readme.md $readmeUrl
    echo "${service}_readme.md" >> src/references/.gitignore

    echo "" >> src/references/index.md
    echo "* $service" >> src/references/index.md
    echo "" >> src/references/index.md
    echo "    - [README](${service}_readme.md)" >> src/references/index.md
    echo "    - [Configuration schema reference]($service.md)" >> src/references/index.md
done
rm -rf tmp
fi

echo "* Clean previous HTML build..."
rm -rf site

echo "* Building HTML..."
mike deploy -F qwc2.yml --push $branch

# cleanup venv
echo "* Clean venv..."
deactivate
rm -rf .venv
