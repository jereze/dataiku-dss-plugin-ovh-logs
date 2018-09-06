all:
	rm -rf dist
	mkdir dist
	zip -r dist/dss-plugin-ovh-logs-import-0.0.5.zip plugin.json python-connectors
