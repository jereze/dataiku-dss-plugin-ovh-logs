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

        print "OVH logs plugin - Start generating rows"
        print "OVH logs plugin - records_limits=%i" % records_limit

        from_date = datetime.datetime.strptime(self.from_date, "%Y-%m-%d")
        to_date = datetime.datetime.strptime(self.to_date, "%Y-%m-%d")

        if to_date < from_date:
            raise ValueError("The end date occurs before the start date")

        # Session object for requests
        s = requests.Session()

        # Test request
        url = 'https://logs.ovh.net/'+str(self.domain)+'/'
        print "OVH logs plugin - Trying to connect to %s" % url
        r = s.get(url, auth = (self.login, self.password))
        if r.status_code == 404:
            raise ValueError('Could not get logs for this domain.')
        elif r.status_code == 401:
            raise ValueError('Authentication error. Check the login and the password.')
        elif r.status_code >= 300:
            raise ValueError('Unknown error with test request.')

        list_datetimes = [from_date + datetime.timedelta(days=x) for x in range((to_date-from_date).days + 1)]
        print "OVH logs plugin - List of dates: %s" % ", ".join([d.strftime("%d/%m/%Y") for d in list_datetimes])

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
            print "OVH logs plugin - %s" % d.strftime("%d/%m/%Y")
            url = 'https://logs.ovh.net/'+str(self.domain)+'/logs/logs-'+str(d.strftime("%m-%Y"))+'/'+str(self.domain)+'-'+str(d.strftime("%d-%m-%Y"))+'.log.gz'
            print "OVH logs plugin - %s - Getting %s" % (d.strftime("%d/%m/%Y"), url)
            r = s.get(url, auth = (self.login, self.password))
            print "OVH logs plugin - %s - Status code: %i" % (d.strftime("%d/%m/%Y"), r.status_code)
            if r.status_code == 200:
                for row in r.text.splitlines():
                    m = pattern.match(row)
                    if m == None:
                        print "OVH logs plugin - %s - No matching for: %s" % (d.strftime("%d/%m/%Y"), row)
                    else:
                        res = m.groupdict()
                        yield res

            else:
                raise ValueError('Error when getting %s' % d.strftime("%d/%m/%Y"))

        print "OVH logs plugin - End generating rows"


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
