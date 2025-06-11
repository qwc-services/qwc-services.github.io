# Tour Guide JSON Configuration

A [DriverJS](https://driverjs.com/) implementation is available in QWC. To configure and use it with the [Tour Guide Plugin](../references/qwc2_plugins.md#tourguide), you can customize your tour guide using a `.json` file.

By default, the file is located in the `static` folder of QWC, but you can also provide any JSON file using the `tourGuideUrl` parameter in the plugin configuration.

Each step of the tour can be configured using the following parameters:

- `selector`: (string) CSS selector to target an element by ID or class.
  **Default**: `null`

- `title`: (string) Title of the tour guide step card.
  **Default**: `""`

- `content`: (string) Content body of the tour guide step card.
  **Default**: `""`

- `side`: (string) Position of the step card relative to the highlighted element. Possible values include `"top"`, `"bottom"`, `"left"`, `"right"`.
  **Default**: `"left"`

- `align`: (string) Alignment of the card relative to its position. Possible values include `"start"`, `"center"`, `"end"`.
  **Default**: `"start"`

- `disableActiveInteraction`: (boolean) Whether to disable user interaction with the highlighted element.
  **Default**: `false`

In addition to the above parameters, it is also possible to configure tasks that will be triggered when moving to the next or previous steps:

- `onNextClick`: (array of strings) A list of actions to perform when the "Next" button is clicked.
- `onPrevClick`: (array of strings) A list of actions to perform when the "Previous" button is clicked.

Supported actions include:

- `"setTask:<taskName>"` – Opens the specified task, or use `null` to close it.
- `"openMenu"` – Opens the main menu.
- `"closeMenu"` – Closes the main menu.
- `"openSubMenu:<submenu>"` – Opens a specific submenu. For example: `"openSubMenu:tools"`

### Example JSON Configuration

```json
[
  {
    "selector": ".Toolbar",
    "title": "Top Bar",
    "content": "The top bar toolbar is a configurable interface managed by the administrator. It hosts many tools available in the QGIS Web Client. Typically, you will find the most frequently used tools here, such as printing and measuring."
  },
  {
    "selector": "button[title='Switch background']",
    "title": "Background Switcher",
    "content": "This module allows you to change the map background. New backgrounds can be configured in the theme configuration file.",
    "side": "top"
  },
  {
    "selector": "#LayerTree",
    "title": "Layer Tree",
    "content": "Here you can manage the visibility and order of the map layers.",
    "onNextClick": ["setTask:null", "openMenu"],
    "onPrevClick": ["setTask:LayerTree", "closeMenu"]
  }
]
```

For a full example, you can refer to the [tourGuide.json](https://github.com/qgis/qwc2/blob/master/static/tourGuide.json) file in the QWC application.
