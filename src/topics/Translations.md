## Translations <a name="translations"></a>

QWC Viewer translations are available for [multiple languags](https://github.com/qgis/qwc2/tree/master/static/translations) (with varying degree of competeness).

By default, QWC will attempt to load the translation matching your browser language. Alternatively, you can explicitly specify the language by adding the `lang=<lang>` query parameter to the application URL, i.e. `lang=de-CH`.

The [Settings Plugin](../references/qwc2_plugins.md#settings) furthermore allows graphically switching the language within QWC, with the list of available languages configured via the `languages` plugin configuration property.

### Translated themes

QWC also supports localized themes, including in particular the theme name, layer and attribute names.

As a prerequisite, the [`get_translations`](https://github.com/qwc-services/qwc-qgis-server-plugins?tab=readme-ov-file#get_translations) QGIS Server plugin needs be enabled, i.e. when using `qwc-qgis-server`:

```yml
  qwc-qgis-server:
    image: docker.io/sourcepole/qwc-qgis-server:<TAG>
    volumes:
      - ./volumes/qgis-server-plugins/get_translations:/usr/share/qgis/python/plugins/get_translations:ro
    ...
```

Then, to localize a theme:

1. In `QGIS → Project Properties → General`, generate a project translation file by selecting the source language and pressing `Generate TS File`.
2. Rename the generated `<projectname>.ts` to `<projectname>_<lang>.ts`, where `<lang>` is language code like `de` or `de-CH`.
3. Open the `<projectname>_<lang>.ts` with the `Qt Linguist` application and fill out the translations. Note that translations need to be marked as "finished" in Qt Linguist

Since the QGIS project translations mechanism does not currently allow translating some project strings which are useful for QWC, these need to be defined in an auxiliary translation file `<projectname>_<lang>.json` structured as follows:
```json
{
  "layouts": {
    "<layout_name>": "<translated_layout_name>",
    ...
  },
  "theme": {
    "title": "<translated_theme_title>"
  }
}
```

Where:

- `layouts` is used to translate print layout names. Note that if you want to translate the name of a (print layout templates)[Printing.md#layout-templates], the `layout_name` may need to include the path portion of the layout (i.e. `<subdir>/<layout_name>`).
- `theme` is used to translate the theme title (and possibly other strings in the future)

Finally, run the `ConfigGenerator` to include the translated theme names in the themes configuration.


### Localized viewer asssets

The `qwc-map-viewer` supports returning localized viewer assets if the `lang=<lang>-<COUNTRY>` query parameter is added to the asset URL, i.e.
```
<baseurl>/assets/myfile.ext?lang=<lang>-<COUNTRY>
```
where `<lang>-<COUNTRY>` is a language-country code like `de-CH`.

The service will then check if `myfile_<lang>-<COUNTRY>.ext` or `myfile_<lang>.ext` exist, returning the first possible match, falling back to `myfile.ext` if neither exists.


### Adding and modifying Viewer translations

When working inside a `qwc-app` source folder, the translations are located at `qwc-app/static/translations`.

A script will take care of merging the translations from the `qwc2` package into the application translations. This way, when updating the `qwc2` dependency, new translations are automatically obtained. This script is automatically invoked on `yarn start`, but can also be manually invoked using

    yarn run tsupdate

Translations are stored inside the respective `translations` folder as regular plain-text JSON files, named `<lang>.json` and can be freely edited with any text editor.

The `tsconfig.json` files stored inside the respective `translations` folder contains the list of languages for which translations should be generated and a list of message IDs to include in the translation. The `tsupdate` script will automatically scan the code for message IDs (looking for static strings passed to `LocaleUtils.tr` and `LocaleUtils.trmsg`), store these in `tsconfig.json` and automatically create resp. update the translation files.

In some cases `tsconfig.json` will not pick up a message ID (for instance, if it is computed at runtime). In these cases, the message IDs can be added manually to the `extra_strings` section of the `tsconfig.json`.

Also it may be desired to override a translation inherited from the QWC components at application level. To prevent `tsupdate` from continuously reverting the overridden translation, the respective message IDs can be added to the `overrides` section in the application `tsconfig.json` file.

To add a new language, list it in `qwc-app/qwc2/translations/tsconfig.json` and run `yarn run tsupdate`, then complete the messages taking the english translation file as reference.

When adding or modifying translations at QWC components level, please contribute them by submitting a pull request to the [upstream qwc2 repository](https://github.com/qgis/qwc2).

### Selectively overriding translation strings

Occasionally, it is desireable to selectively override specific translation strings. While one can modify the full translation file as described above, especially when using the `qwc-map-viewer` docker image, it is easier to just selectively override the desired translation strings and leave the original file unchanged and avoid having to compile a custom viewer (or overwriting the entire file with a docker volume mount).

To do this:

* Set `loadTranslationOverrides` to `true` in `config.json`.
* Create a `<lang>_overrides.json` containing just the ovverridden strings, for example `en-US_overrides.json`:
```json
{
  "messages": {
    "appmenu": {
      "items": {
        "LayerTree": "Layers"
      }
    }
  }
}
```
* Place this file inside the `translations` folder of your production build. When using `qwc-docker`, you can place this file in `qwc-docker/volumes/qwc2/translations/` and mount this file inside the container, i.e. :
```yml
qwc-map-viewer:
  image: sourcepole/qwc-map-viewer:vYYYY.MM.DD
  [...]
  volumes:
    - ./volumes/qwc2/translations/en-US_overrides.json:/qwc2/translations/en-US_overrides.json:ro
```

### Specifying the default fallback translation

When no translation exists for the requested language (i.e. the current browser language), QWC will fall back to the default translation specified as `defaultLocaleData` in `qwc2-app/js/appConfig.js`. For the stock application, the default fallback translation is `en-US`.
