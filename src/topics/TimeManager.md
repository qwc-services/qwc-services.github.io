# Temporal layers (Time Manager)

QWC supports WMS layers with time dimension (WMS-T) through the [`TimeManager`](../references/qwc2_plugins.md#timemanager) plugin.

![Time Manager](../images/timemanager.jpg?style=centerme)

To view and manage temporal layers in QWC, add a new time dimension, selecting appropriate temporal fields as start- and end-attributes in the QGIS Layer Properties &rarr; QGIS Server &rarr; Dimensions.

For the time markers functionality in the Time Manager plugin to work correctly, you also need to [enable](../configuration/ServiceConfiguration.md#enabling-services) the [`qwc-feature-info-service`](https://github.com/qwc-services/qwc-feature-info-service).

*Note:* The QGIS Layer Properties &rarr; Temporal settings are ignored by QGIS Server and hence have no effect in QWC.

