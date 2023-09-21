# FAQ

## Changing the `qwc-docker` port

In the default setup, `qwc-docker` will run on port `8088`. To change this, you can modify the `api-gateway` port mapping in `docker-compose.yml`, i.e. to run on port `1234`:

    qwc-api-gateway:
        image: nginx:1.19
        ports:
          - "1234:80"

