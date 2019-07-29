# -*- coding: latin_1 -*-
import fastjsonschema
import json
import os
from pprint import pprint

from cloudant import Cloudant


class CloudantCommunities:
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
            self.client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'],
                                   url=os.environ['CLOUDANT_URL'], connect=True)
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

    @staticmethod
    def validate_resilience_object(resilience_object):
        schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "RESILIENCIA": {
                    "type": "object",
                    "properties": {
                        "badges": {
                            "type": "array",
                            "items": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "badge_id": {
                                            "type": "integer"
                                        },
                                        "description": {
                                            "type": "string"
                                        },
                                        "date": {
                                            "type": "string"
                                        },
                                        "type": {
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "badge_id",
                                        "description",
                                        "date",
                                        "type"
                                    ]
                                }
                            ]
                        },
                        "stage": {
                            "type": "integer"
                        },
                        "step": {
                            "type": "integer"
                        },
                        "resilience_stage_level": {
                            "type": "number"
                        },
                        "resilience_total_level": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "badges",
                        "stage",
                        "step",
                        "resilience_stage_level",
                        "resilience_total_level"
                    ]
                }
            },
            "required": [
                "RESILIENCIA"
            ]
        }
        validate = fastjsonschema.compile(schema)
        validate(resilience_object)

    def get_document_by_id(self, doc_id):
        doc = None
        if type(doc_id) != 'str':
            doc_id = str(doc_id)
        print(type(doc_id))
        try:
            doc = self.db[doc_id]
        except:
            pass
        return doc

    def save_new_document(self, data):
        if self.client:
            data['_id'] = str(data['POBLAC_ID'])
            my_document = self.db.create_document(data)
            # return jsonify(data)
            return data
        else:
            print('No database')
            # return jsonify(data)
            return data

    @staticmethod
    def update_document(data, document):
        data['_rev'] = document['_rev']
        document.update(data)
        document.save()
        # return jsonify(data)
        return data

    def update_document_or_save_if_new(self, data):
        try:
            document_in_database = self.get_document_by_id(data['POBLAC_ID'])
        except KeyError:
            document_in_database = None
        if document_in_database is not None:
            data = self.update_document(data, document_in_database)
        else:
            data = self.save_new_document(data)
        # return jsonify(data)
        return data


def test_sample():
    sample = {'POBLAC_ID': 602004,
              'PUEBLO': 'MACACONA,ESPARZA,PUNTARENAS',
              'RESILIENCIA': {'badges': [{'description': 'First Badge',
                                          'icon': 'url_for_image',
                                          'title': 'Beginner'},
                                         {'description': 'Second Badge',
                                          'icon': 'url_for_image',
                                          'title': 'Second Runner'},
                                         {'description': 'Third Badge',
                                          'icon': 'url_for_image',
                                          'title': 'Third Runner'},
                                         {'description': 'Fourth Badge',
                                          'icon': 'url_for_image',
                                          'title': 'Fourth Runner'}],
                              'resilience_level': 0.9}}
    return sample


def main():
    cloud_db = CloudantCommunities()
    sample_data = test_sample()
    save = cloud_db.update_document_or_save_if_new(sample_data)
    macacona = cloud_db.get_document_by_id(sample_data["POBLAC_ID"])
    pprint(macacona)


if __name__ == "__main__":
    main()
