# coding=latin_1
from cloudant import Cloudant
import os
import json
from pprint import pprint

class Cloudant_Communities:
    def __init__(self):
        self.db_name = 'resilapp-communities-badges'
        self.client = None
        self.db = None
        if 'VCAP_SERVICES' in os.environ:
            self.vcap = json.loads(os.getenv('VCAP_SERVICES'))
            if 'cloudantNoSQLDB' in self.vcap:
                self.creds = self.vcap['cloudantNoSQLDB'][0]['credentials']
                self.user = self.creds['username']
                self.password = self.creds['password']
                self.url = 'https://' + self.creds['host']
                self.client = Cloudant(self.user, self.password, url=self.url, connect=True)
                self.db = self.client.create_database(self.db_name, throw_on_exists=False)
        elif "CLOUDANT_URL" in os.environ:
            self.client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
            self.db = self.client.create_database(self.db_name, throw_on_exists=False)
        elif os.path.isfile('vcap-local.json'):
            with open('vcap-local.json') as f:
                self.vcap = json.load(f)
                self.creds = self.vcap['services']['cloudantNoSQLDB'][0]['credentials']
                self.user = self.creds['username']
                self.password = self.creds['password']
                self.url = 'https://' + self.creds['host']
                self.client = Cloudant(self.user, self.password, url=self.url, connect=True)
                self.db = self.client.create_database(self.db_name, throw_on_exists=False)


    def get_document_by_id(self, id):
        return self.db[id]


def main():
    cloud_db = Cloudant_Communities()
    doc = cloud_db.get_document_by_id("614a652ef7c88856b3d26d7c58f5ca62")
    pprint(doc)


if __name__=="__main__":
    main()
