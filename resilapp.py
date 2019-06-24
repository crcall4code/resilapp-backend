from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

app = Flask(__name__, static_url_path='')

db_name = 'resilapp-communities'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('community-index.html')


# /**
#  * Endpoint to get a JSON array of all the communities in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/communities
#  * </code>
#  * @return An array of all the communities data
#  */
@app.route('/api/communities', methods=['GET'])
def get_communities():
    if client:
        return jsonify(list(map(lambda doc: doc, db)))
    else:
        print('No database')
        return jsonify([])

@app.route('/api/communities/<community>', methods=['GET'])
def get_community(community):
    if client:
    	community_list = list(map(lambda doc:(doc if doc['name']==community else None), db))
    	community_list = [i for i in community_list if i!=None]
        return jsonify(community_list)
    else:
        print('No database')
        return jsonify([])

# /* Endpoint to add a new community to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Community Name",
#		"ubication_x": Longitude_As_Number,
#		"ubication_y": Latitude_As_Number,
#		"province": Province or State,
#		"canton": City,
#		"resilience": {Resilience_Object}
# * }
# */
# /* A Resilience_Object will contain:
#	{
#		"resilience_level":Decimal_Number_From_Zero_To_One,
#		"badges":[{				------> This one is a list, containing one or several ResilienceBadge_Object(s)
#			"title":"Beginner",
#			"description":"First Badge",
#			"icon":"url_for_image"
#	}
#*/
@app.route('/api/communities', methods=['POST'])
def put_community():
    name = request.json['name']
    ubication_x = request.json['ubication_x']
    ubication_y = request.json['ubication_y']
    province = request.json['province']
    canton = request.json['canton']
    resilience = request.json['resilience']
    data = {
    		'name':name,
    		'ubication_x':ubication_x,
			'ubication_y':ubication_y,
			'province':province,
			'canton':canton,
			'resilience':resilience
    		}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
