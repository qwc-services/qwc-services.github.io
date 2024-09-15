# New qwc-document-service, jasper-reporting-service obsolete

As of 2024.09.15, the `jasper-reporting-service` is obsolete, its functionality has been integrated into the `qwc-document-service`. Check out the new [Reports](../topics/Reports.md) chapter to learn more about integrating the reporting functionality into QWC2.

# Split categorized layers functionality rewritten as QGIS Server plugin

As of 2024.02.02 the split categorized layers functionality previously part of `qwc-config-generator` has been rewritten as a [QGIS Server plugin](https://github.com/qwc-services/qwc-qgis-server-plugins/tree/main/split_categorized).

This greatly simplifies the handling of such projects. The `-noqgis` image tag suffix in `qwc-config-generator:vXXXX-noqgis` has been dropped resp. shipped as the regular `qwc-config-generator:vXXXX` docker images.

See the [categorized layers documentation](https://qwc-services.github.io/master/configuration/ThemesConfiguration/#split-categorized-layers) for instructions how to configure the new `split_categorized` plugin.

# Updating to qwc-data-service v2024.05.21

The `qwc-data-service` version 2024.05.21 introduces two now logging fields `create_user_field` and `create_timestamp_field`. Record creation will now be logged to these fields, if set, and record updates will be logged to `edit_user_field` and `edit_timestamp_field`. Previously, both record creation and updates were logged to `edit_user_field` and `edit_timestamp_field`. As of v2024.05.21, you need to set `create_user_field` and `create_timestamp_field` (also to the same values as `edit_user_field` and `edit_timestamp_field`) if you want to log creation.

# 2023.10.24 qwc-base-db rework \[2023-lts &rarr; 2024-lts\]

As of 2023.10.24 the QWC base DB image has been reworked as follows:

* Migrations were moved to the `qwc-base-db` repository, the `qwc-config-db` repository is now obsolete.
* A new `qwc-base-db-migrate` image helps migrating dockerized or external config DBs.
* Demo data will be initialized by an optional setup script in `qwc-docker`, the `qwc-demo-db` repository is now obsolete.

To use the new images, replace

```yml
  qwc-postgis:
    image: docker.io/sourcepole/qwc-demo-db:<version>
  ...
```

with

```yml
  qwc-postgis:
    image: sourcepole/qwc-base-db:<pg_version>
    environment:
      POSTGRES_PASSWORD: '' # TODO: Set your postgres password here!
    volumes:
     - ./volumes/db:/var/lib/postgresql/docker
     # If you don't want/need the demo data, you can remove this line
     - ./volumes/demo-data/setup-demo-data.sh:/docker-entrypoint-initdb.d/2_setup-demo-data.sh
    ports:
     - "127.0.0.1:5439:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s

  qwc-config-db-migrate:
    image: sourcepole/qwc-base-db-migrate:<version>
    volumes:
     - ./pg_service.conf:/tmp/pg_service.conf:ro
    depends_on:
     - qwc-postgis
```

in your `docker-compose.yml`.

Note:

- It is now mandatory to set your own `POSTGRES_PASSWORD`.
- You can keep your previous `volumes/db` postgres data folder, but it is recommended to make a backup.
* The `sourcepole/qwc-base-db` images are versioned according to the Postgres major version (i.e. 13, 14, 15, ...).
* The `sourcepole/qwc-base-db-migrate` images are versioned by date (`vYYYY.MM.DD`)
- See the [`qwc-base-db` README](https://github.com/qwc-services/qwc-base-db) for more information.
- As of `2023.10.24` the name of the database was changed to the more generic `qwc_services` instead of `qwc_demo`.

# Upgrading to qwc service images v2022.01.26

The `qwc-uwsgi-base` images have been changed to allow for configurable UID/GID of the `uwsgi` process. The default is `UID=33` and `GID=33`, you can override it by setting the `SERVICE_UID` and `SERVICE_GID` environment variables in `docker-compose.yml`.

As a consequence, `/var/www` is not necessarily anymore the home directory of the user wich runs `uwsgi`, and therefore the `qwc-uwsgi-base` images now set `ENV PGSERVICEFILE="/srv/pg_service.conf"`. You'll therefore need to adapt your `pg_service.conf` volume mounts in your `docker-compose.yml` to point to that location, i.e.

    [...]
    - ./pg_service.conf:/srv/pg_service.conf:ro
    [...]

# Upgrading to qwc-config-generator-v2022.01.12

- `scanned_projects_path_prefix` has been dropped as a config setting. Instead, `qgis_projects_scan_base_dir` must be a directory below `qgis_projects_base_dir`, and the prefix is automatically computed internally.
- `scanned_projects_path_prefix` has been added as a config setting as the output path for preprocessed qgis projects. It must be a directory below `qgis_projects_base_dir` to which the config service is allowed to write.

# Upgrading from qwc service images v2021.x to v2022.01.08 or later

Starting with v2022.01.08, the requirements of all services where updated to use Flask-JWT-Extended 4.3.1.

Flask-JWT-4.x changes the JWT format (see [4.0.0 Breaking Changes](https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#encoded-jwt-changes-important)), which can result in QWC Services returning a `Missing claim: identity` error message.

To avoid this:
* Change your JWT secret key in `.env`.
* Ensure all services are upgraded to v2022.01.12 or later (if such a version exists). Please omit v2022.01.08 and v2022.01.11.
