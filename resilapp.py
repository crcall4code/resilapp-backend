# coding=latin_1
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
from SQL_Database import DB2_Towns, DB2_Communities
from Cloudant_DB import Cloudant_Communities

app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

cloudant_db = Cloudant_Communities()

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

# /* Endpoint to add a new community to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Community Name",
#       "ubication_x": Longitude_As_Number,
#       "ubication_y": Latitude_As_Number,
#       "province": Province or State,
#       "city": City,
#       "resilience": {Resilience_Object}
# * }
# */
# /* A Resilience_Object will contain:
#   {
#       "resilience_level":Decimal_Number_From_Zero_To_One,
#       "badges":[{             ------> This one is a list, containing one or several ResilienceBadge_Object(s)
#           "title":"Beginner",
#           "description":"First Badge",
#           "icon":"url_for_image"
#   }
#*/
@app.route('/api/communities', methods=['POST', 'GET'])
def communities():
    if request.method == 'GET':
        if cloudant_db.client:
            cloudant_db.db = "resilapp-communities"
            return jsonify(list(map(lambda doc: doc, cloudant_db.db)))
        else:
            print('No database')
            return jsonify([])
    elif request.method == 'POST':
        name = request.json['name']
        ubication_x = request.json['ubication_x']
        ubication_y = request.json['ubication_y']
        province = request.json['province']
        city = request.json['city']
        resilience = request.json['resilience']
        data = {
                'name':name,
                'ubication_x':ubication_x,
                'ubication_y':ubication_y,
                'province':province,
                'city':city,
                'resilience':resilience
                }
        if cloudant_db.client:
            cloudant_db.db = "resilapp-communities"
            my_document = cloudant_db.db.create_document(data)
            data['_id'] = my_document['_id']
            return jsonify(data)
        else:
            print('No database')
            return jsonify(data)


@app.route('/api/communities/<community>', methods=['GET'])
def get_community(community):
    if cloudant_db.client:
        cloudant_db.db = "resilapp-communities"
        community_list = list(map(lambda doc:(doc if doc['name']==community else None), cloudant_db.db))
        community_list = [i for i in community_list if i!=None]
        return jsonify(community_list)
    else:
        print('No database')
        return jsonify([])


@app.route('/api/communities/<province>/<city>/<town>', methods=['POST'])
def put_community(province, city, town):
    db_towns = DB2_Towns.getInstance()
    db_communities = DB2_Communities.getInstance()
    town = db_towns.select_Town_dictionary_by_State_City_and_Name(province, city, town)
    POBLAC_ID = town["POBLAC_ID"]
    PUEBLO = "{},{},{}".format(town["PUEBLO"],town["CANTON"],town["PROVINCIA"])
    RESILIENCIA = request.json['RESILIENCIA']
    data = {
            'POBLAC_ID':POBLAC_ID,
            'PUEBLO':PUEBLO,
            'RESILIENCIA':RESILIENCIA
            }
    if cloudant_db.client:
        cloudant_db.db_name = 'resilapp-communities-badges'
        cloudant_db.db = client.create_database(cloudant_db.db_name, throw_on_exists=False)
        my_document = cloudant_db.db.create_document(data)
        data['_id'] = my_document['_id']
        community = list(map(lambda doc:(doc if doc['POBLAC_ID']==POBLAC_ID else None), cloudant_db.db))
        community = [i for i in community if i!=None]
        community = community[0]
        town['RESILIENCIA'] = dict(_id=community['_id'],_rev=community['_rev'])
        db_communities.insert_Community(town)
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)


@app.route('/api/towns/provinces', methods=['GET'])
def get_provinces():
    db = DB2_Towns.getInstance()
    provinces = db.select_all_States()
    return jsonify(provinces)

@app.route('/api/towns/<province>', methods=['GET'])
def get_cities(province):
    db = DB2_Towns.getInstance()
    cities = db.select_all_Cities_by_State(province)
    return jsonify(cities)

@app.route('/api/towns/<province>/<city>', methods=['GET'])
def get_towns(province,city):
    db = DB2_Towns.getInstance()
    towns = db.select_all_Towns_by_State_and_City(province, city)
    return jsonify(towns)


@app.route('/api/towns/<province>/<city>/<town>', methods=['GET'])
def get_poblado(province,city,town):
    db = DB2_Towns.getInstance()
    town = db.select_Town_dictionary_by_State_City_and_Name(province, city, town)
    return jsonify(town)


@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
