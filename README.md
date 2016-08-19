# OVH logs importer

This plugin helps you to import in [Dataiku DSS](http://www.dataiku.com/dss/) the logs of your website hosted by [OVH shared hosting](http://www.ovh.com).

Read more on the plugin page on Dataiku website: https://www.dataiku.com/dss/plugins/info/ovh-logs-import.html

Read OVH documentation to get access to your logs:

* English: https://www.ovh.co.uk/g1344.statistiques-logs
* French: https://www.ovh.com/fr/g1344.statistiques-et-logs

## How to set-up

* Browse to the Plugins Marketplace in DSS administration tab and install the plugin in DSS. Or, you can download the zip ([dss-plugin-ovh-logs-import-0.0.3.zip](https://github.com/jereze/dataiku-dss-plugin-ovh-logs/releases/download/v0.0.3/dss-plugin-ovh-logs-import-0.0.3.zip)) and upload it in DSS adminitration tab.
* Create a new dataset with this connector. Fill the parameters and click on the “Test” button. Then, save and explore.

## Logs

To debug:

`tail -fn 100 data_dir/run/backend.log | egrep 'OVH logs plugin'`

## Changelog

**Version 0.0.3 (2015-11-12)**

* Fix fields in `connector.json`

The plugin is compatible DSS 2.2.0 released today. This version of DSS brings a ton of enhancements to the plugins system and fix some bugs. It is highly recommended to use the plugin from this version.

**Version 0.0.2 (2015-11-05)**

* Test request to check the connection
* More logs for better debugging

**Version 0.0.1 (2015-11-03)**

* Initial release
