# Quick start

## Running QWC2 as part of qwc-services

`qwc-services` is a collection of loosely coupled micro-services for extending QWC2. The services communicate with each other via HTTP/Rest, and are mostly written in Python.

The easiest way to run `qwc-services` is to use the readily available docker images, using the sample setup at [qwc-docker](https://github.com/qwc-services/qwc-docker).

To be able to run `qwc-docker`, first install `docker` and `docker compose`:

- Docker: <https://docs.docker.com/engine/install/>
- docker-compose: <https://docs.docker.com/compose/install/>

Then, follow these steps:

- Clone the qwc-docker sample setup at [qwc-docker](https://github.com/qwc-services/qwc-docker) and copy the docker-compose and api-gateway configuration templates:
```bash
git clone https://github.com/qwc-services/qwc-docker.git
cd qwc-docker
cp docker-compose-example.yml docker-compose.yml
cp api-gateway/nginx-example.conf api-gateway/nginx.conf
```
- Set the password for the `postgres` superuser in `docker-compose.yml`:
```yml
  qwc-postgis:
    image: sourcepole/qwc-base-db:<version>
    environment:
      POSTGRES_PASSWORD: '<SET YOUR PASSWORD HERE>'
```
- Create a secret key:
```bash
python3 -c 'import secrets; print("JWT_SECRET_KEY=\"%s\"" % secrets.token_hex(48))' >.env
```
- Change the UID/GID which runs the QWC services to match the user/group which owns the shared volumes on the host by setting `SERVICE_UID` and `SERVICE_GID` in `qwc-docker/docker-compose.yml`.

- Set permissions for the shared solr data volume:
```bash
sudo chown 8983:8983 volumes/solr/data
```
- Start all containers (will download all images from dockerhub when executed the first time):
```bash
docker-compose up
```

*Note*: If using the newer `docker compose` project, you need to write `docker compose up` instead of `docker-compose up` (and similarly for other `docker-compose` calls).

*Note*: The sample `docker-compose-example.yml` uses `latest-YYYY-lts` as image versions. It is recommended to replace these with a fix version tag when deploying the application to prevent docker from automatically pulling new versions when the application is launched, which may be undesired. See [Keeping QWC services up to date](configuration/../configuration/ServiceConfiguration.md#upgrading).

The map viewer will run on <http://localhost:8088/>.

The admin GUI will run on <http://localhost:8088/qwc_admin> (default admin credentials: username `admin`, password `admin`, requires password change on first login).

Next steps:

- [Configure the themes](configuration/ThemesConfiguration.md)
- [Customize the viewer](configuration/ViewerConfiguration.md)
- [Configuring the services](configuration/../configuration/ServiceConfiguration.md)
- [Set resource permissions](configuration/ResourcesPermissions.md)

## Running QWC2 as a standalone viewer

If you don't need the advanced functionalities provided by `qwc-services` or want to integrate QWC2 in another environment, you can run QWC2 as a standalone viewer.

To work with QWC2, you will need a minimal development environment consisting of [git](https://git-scm.com/), [node](https://nodejs.org/) and [yarn](https://yarnpkg.com). You will also need a running QGIS Server instance which serves your projects.

The fastest way to get started is by cloning the demo application:
```bash
git clone --recursive https://github.com/qgis/qwc2-demo-app.git
```
Next, install all required dependencies:
```bash
cd qwc2-demo-app
yarn install
```
Then, start a local development application:
```bash
yarn start
```
The development application will run by default on <http://localhost:8081>.

At this point, you can customize and configure the application according to your needs, as described in detail in the following chapters.

The final step is to compile a deployable application bundle for production:
```bash
yarn run prod
```
You can then deploy the contents of the `prod` folder to your web server.

Next steps:

- [Configure the themes](configuration/ThemesConfiguration.md)
- [Customize the viewer](configuration/ViewerConfiguration.md)
