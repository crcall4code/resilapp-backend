# -*- coding: latin_1 -*-
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
from SQL_Database import DB2_Towns, DB2_Communities, DB2_Resilience_Steps
from Cloudant_DB import Cloudant_Communities

app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

cloudant_db = Cloudant_Communities()

@app.route('/')
def root():
    return app.send_static_file('community-index.html')

# /* A Resilience_Object will contain:
#   {
#       "resilience_level":Decimal_Number_From_Zero_To_One,
#       "badges":[{             ------> This one is a list, containing one or several ResilienceBadge_Object(s)
#           "title":"Beginner",
#           "description":"First Badge",
#           "icon":"url_for_image"
#   }
#*/

@app.route('/api/communities/<community_id>', methods=['GET'])
def get_community_resilience(community):
    communityResilience = cloudant_db.get_document_by_id(community_id) 
    return jsonify(communityResilience)
    
@app.route('/api/communities/<province>/<city>/<town>', methods=['POST', 'GET'])
def community_and_resilience(province, city, town):
    if request.method == 'GET':
        db_towns = DB2_Towns.getInstance()
        db_communities = DB2_Communities.getInstance()
        town = db_towns.select_Town_dictionary_by_State_City_and_Name(province, city, town)
        community = db_communities.select_community_Dictionary_by_Poblac_ID(town['POBLAC_ID'])
        print("COMUNIDAD:",community)
        if community!=None:
            resiliencia = cloudant_db.get_document_by_id(community['POBLAC_ID'])
            print("RESILIENCIA:",resiliencia)
            community['RESILIENCIA'] = resiliencia
        return jsonify(community)
    elif request.method == 'POST':
        db_towns = DB2_Towns.getInstance()
        db_communities = DB2_Communities.getInstance()
        db_resilience_steps = DB2_Resilience_Steps.getInstance()
        town = db_towns.select_Town_dictionary_by_State_City_and_Name(province, city, town)
        community = dict(POBLAC_ID=town['POBLAC_ID'])
        community['PUEBLO'] = "{},{},{}".format(town["PUEBLO"],town["CANTON"],town["PROVINCIA"])
        db_communities.insert_Community(community)
        resiliencia = request.json['RESILIENCIA']
        stage = resiliencia['RESILIENCIA']['stage']
        step = resiliencia['RESILIENCIA']['step']
        total_and_stage_percentages = db_resilience_steps.get_accomplished_percentages_total_and_stage(stage, step)
        resiliencia['resilience_stage_level'] = str(total_and_stage_percentages['Stage'])
        resiliencia['resilience_total_level'] = str(total_and_stage_percentages['Total'])
        save = cloudant_db.update_document_or_save_if_new(resiliencia)
        return jsonify(save)

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
