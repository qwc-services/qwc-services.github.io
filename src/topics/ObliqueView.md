# Oblique aerial imagery

QWC allows displaying oblique aerial imagery via the [ObliqueView](../references/qwc2_plugins.md#obliqueview) plugin and the [qwc-oblique-imagery-service](https://github.com/qwc-services/qwc-oblique-imagery-service).

If you are using `qwc-docker`, you can set up the `qwc-oblique-imagery-service` as follows:
```yml
  qwc-oblique-imagery-service:
    image: docker.io/sourcepole/qwc-oblique-imagery-service:<tag>
    environment:
      <<: *qwc-service-variables
      SERVICE_MOUNTPOINT: '/api/v1/oblique-imagery'
    volumes:
      - ./volumes/config:/srv/qwc_service/config:ro
      - ./volumes/oblique-images:/images:ro
```

Remember to also add the corresponding route to the `api-gateway/nginx.conf`.

Finally, set the `obliqueImageryServiceUrl` in the viewer `config.json`, i.e. to `/api/v1/oblique-imagery`.

## Configuring the oblique aerial imagery datasets

Aerial imagery datasets are expected to be provided as georeferenced TIFF images (where the georeferencing is cleary an approximation since the images are shot from an oblique camera).

Places these images below `volumes/oblique-images/<dataset_name>`, and configure the dataset in the `obliqueImagery` service section in the `tenantConfig.json`:
```json
    {
      "name": "obliqueImagery",
      "config": {},
      "resources": {
        "oblique_image_datasets":[
          {
            "name": "<dataset_name>",
            "crs": "<epsg_code>",
            "pattern_north":"*_North_*.tif",
            "pattern_east":"*_East_*.tif",
            "pattern_south":"*_South_*.tif",
            "pattern_west":"*_West_*.tif"
          }
        ]
      }
    }
```

The images shot in the four cardinal directions are distinguished by the `pattern_*` settings.

Finally, configure the available oblique datasets for desired themes in the `themesConfig.json` as follows:
```json
    {
      "url": "<wms_url>",
      "title": "<theme title>",
      ...
      "obliqueDatasets": [
        {
          "dataset": "<dataset_name>",
          "default": <false|true>,
          "backgroundLayer": "<background_layer_name>",
          "backgroundOpacity": <0-255>,
          "title": "<dataset_title>",
          "titleMsgId": "<dataset_title_msgid>"
        },
        ...
      ]
    }
```
Where:

* `dataset` is must be set to a dataset configured in `tenantConfig.json`
* `default` denotes whether the dataset displayed by default (relevant if multiple datasets are configured)
* `backgroundLayer` is the name of a background layer, as also used in the `backgroundLayers` section of the theme configuration
* `backgroundOpacity` specifies the opacity of the background layer (`0` is transparent, `255` is fully opaque)
* `title` resp. `titleMsgId` specify the title resp. title translation message id of the dataset as displayed in the dataset switcher in QWC.

### Permissions <a name="permissions"></a>

To restrict oblique datasets, create a `Oblique Image Dataset` resource named according to the name of the dataset and create permissions assigning the desired roles to the resources.
