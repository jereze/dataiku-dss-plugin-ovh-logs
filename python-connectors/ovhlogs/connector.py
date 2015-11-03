from dataiku.connector import Connector
import requests
import datetime
import re

class MyConnector(Connector):

    def __init__(self, config):
        Connector.__init__(self, config)  # pass the parameters to the base class

        # perform some more initialization
        self.login = self.config.get("login")
        self.password = self.config.get("password")
        self.domain = self.config.get("domain")
        self.from_date = self.config.get("from_date")
        self.to_date = self.config.get("to_date")

    def get_read_schema(self):
        """
        Returns the schema that this connector generates when returning rows.

        The returned schema may be None if the schema is not known in advance.
        In that case, the dataset schema will be infered from the first rows.

        Whether additional columns returned by the generate_rows are kept is configured
        in the connector.json with the "strictSchema" field
        """
        return None

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                            partition_id=None, records_limit = -1):
        """
        The main reading method.

        Returns a generator over the rows of the dataset (or partition)
        Each yielded row must be a dictionary, indexed by column name.

        The dataset schema and partitioning are given for information purpose.
        """

        from_date = datetime.datetime.strptime(self.from_date, "%Y-%m-%d")
        to_date = datetime.datetime.strptime(self.to_date, "%Y-%m-%d")

        if to_date < from_date:
            raise ValueError("The end date occurs before the start date")

        list_datetimes = [from_date + datetime.timedelta(days=x) for x in range((to_date-from_date).days + 1)]

        parts = [
            r'(?P<host>\S+)',                   # host %h
            r'\S+',                             # indent %l (unused)
            r'(?P<user>\S+)',                   # user %u
            r'\[(?P<time>.+)\]',                # time %t
            r'"(?P<request>.+)"',               # request "%r"
            r'(?P<status>[0-9]+)',              # status %>s
            r'(?P<size>\S+)',                   # size %b (careful, can be '-')
            r'"(?P<referer>.*)"',               # referer "%{Referer}i"
            r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
        ]
        pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

        for d in list_datetimes:
            print "OVH logs plugin - Working on %s" % d.strftime("%d/%m/%Y")
            r = requests.get('https://logs.ovh.net/'+str(self.domain)+'/logs-'+str(d.strftime("%m-%Y"))+'/'+str(self.domain)+'-'+str(d.strftime("%d-%m-%Y"))+'.log.gz', auth = (self.login, self.password))
            print "OVH logs plugin - Getting %s" % r.url
            print "OVH logs plugin - Status code: %i" % r.status_code
            if r.status_code == 200:
                for row in r.text.splitlines():
                    m = pattern.match(row)
                    res = m.groupdict()
                    yield res

            elif r.status_code == 401:
                raise ValueError('Error when authenticating. Check the login and the password.')
            else:
                raise ValueError('Error when getting %s' % d.strftime("%d/%m/%Y"))



    def get_writer(self, dataset_schema=None, dataset_partitioning=None,
                         partition_id=None):
        """
        Returns a write object to write in the dataset (or in a partition)

        The dataset_schema given here will match the the rows passed in to the writer.

        Note: the writer is responsible for clearing the partition, if relevant
        """
        raise Exception("Unimplemented")


    def get_partitioning(self):
        """
        Return the partitioning schema that the connector defines.
        """
        raise Exception("Unimplemented")

    def get_records_count(self, partition_id=None):
        """
        Returns the count of records for the dataset (or a partition).

        Implementation is only required if the field "canCountRecords" is set to
        true in the connector.json
        """
        raise Exception("unimplemented")
