# OVH logs importer

This plugin helps you to import in [Dataiku Data Science Studio](http://www.dataiku.com/dss/) the logs of your website hosted by [OVH shared hosting](http://www.ovh.com).

Read OVH documentation to get access to your logs:

* English: https://www.ovh.co.uk/g1344.statistiques-logs
* French: https://www.ovh.com/fr/g1344.statistiques-et-logs

# How to set-up

* Install python dependencies with the [pip of the DSS virtualenv](http://learn.dataiku.com/howto/code/python/install-python-packages.html): `data_dir/bin/pip install --upgrade requests`
* Install the plugin in DSS.
* Create a new dataset with this connector. Fill the parameters and click on the “Test“ button. Then, save and explore.

