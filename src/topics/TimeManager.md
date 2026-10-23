# Temporal layers (Time Manager)

QWC supports WMS layers with time dimension (WMS-T) through the [`TimeManager`](../references/qwc2_plugins.md#timemanager) plugin.

![Time Manager](../images/timemanager.jpg?style=centerme)

To view and manage temporal layers in QWC, add a new time dimension, selecting appropriate temporal fields as start- and end-attributes in the QGIS Layer Properties &rarr; QGIS Server &rarr; Dimensions.

The time markers functionality in the Time Manager plugin requires the `qwc-ogc-service` to work correctly.

*Note:*

- An end-time attribute must be specified, or else the QGIS Server won't render any feature even if the passed time dimension is greater than the start-time attribute. If your data does not have an end attribute, you can for instance create a view which adds an end attribute with value i.e. `now()` or a value far in the future.
- The QGIS Layer Properties &rarr; Temporal settings are ignored by QGIS Server and hence have no effect in QWC.

