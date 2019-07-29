# -*- coding: latin_1 -*-
import atexit
import os

from jsonschema.exceptions import ValidationError, FormatError, SchemaError
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
from jinja2.exceptions import TemplateNotFound

from Cloudant_DB import CloudantCommunities
from SQL_Database import Db2Database

app = Flask(__name__, static_url_path='', template_folder='templates')
Bootstrap(app)
CORS(app)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

cloudant_db = CloudantCommunities()
sql_db = Db2Database.get_instance()


# *********************************** WEB PAGES ********************************************
def render_page(page_name):
    try:
        page = render_template(page_name)
    except TemplateNotFound:
        page = not_found(404)
    return page


@app.route('/')
def root():
    return render_page('index.html')


@app.route('/comunidades')
def comunidades():
    return render_page('comunidades.html')


@app.route('/consultar-comunidad/<province>/<canton>/<community>')
def query_comunidades(province, canton, community):
    return render_template('consultar-comunidad.html', province=province, canton=canton, community=community)


@app.route('/consultar-comunidad')
def consultar_comunidad():
    return render_page('consultar-comunidad.html')


@app.route('/poblados')
def poblados():
    return render_page('poblados.html')


@app.route('/town_tables')
def town_tables():
    return render_page('town_tables')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


# ******************************* DATABASE FUNCTIONS ***************************************

@app.route('/api/communities/<community_id>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_community_resilience(community_id):
    community_resilience = cloudant_db.get_document_by_id(community_id)
    if not community_resilience:
        community_resilience = "Comunidad no encontrada, revise su ID."
    return jsonify(community_resilience)


@app.route('/api/communities/<province>/<city>/<town>', methods=['POST', 'GET'])
@cross_origin(send_wildcard=True)
def community_and_resilience(province, city, town):
    if request.method == 'GET':
        town = sql_db.select_town_dictionary_by_state_city_and_name(province, city, town)
        try:
            community = sql_db.select_community_dictionary_by_poblac_id(town['POBLAC_ID'])
        except TypeError:
            community = None
        if community is not None:
            resiliencia = cloudant_db.get_document_by_id(community['POBLAC_ID'])
            print("RESILIENCIA:", resiliencia)
            community['RESILIENCIA'] = resiliencia['RESILIENCIA']['RESILIENCIA']
        else:
            community = dict(
                PUEBLO="No existe en base de datos.",
                POBLAC_ID="N/A",
                RESILIENCIA=dict(
                    badges=[],
                    resilience_stage_level=0,
                    resilience_total_level=0,
                    stage=1,
                    step=1
                )
            )
        return jsonify(community)
    elif request.method == 'POST':
        db_resilience_steps = sql_db.get_resilience_instance()
        # Get town from SQL database, to avoid saving non existent towns
        town = sql_db.select_town_dictionary_by_state_city_and_name(province, city, town)
        # Create community SQL database object from town object
        community = dict(POBLAC_ID=town['POBLAC_ID'])
        community['PUEBLO'] = "{},{},{}".format(town["PUEBLO"], town["CANTON"], town["PROVINCIA"])
        # Get object containing community resilience from request,
        # the main key must be "RESILIENCIA"
        resiliencia_from_request = request.json['RESILIENCIA']
        # Subsequent keys:
        #   POBLAC_ID (from database query above)
        #   PUEBLO (concatenation, from database query above)
        #   RESILIENCIA(
        #               badges[(
        #                      badge_id,
        #                      description,
        #                      date,
        #                      type:step/badge
        #                      )];
        #               current_stage;
        #               current_step;
        #               resilience_stage_level(%);
        #               resilience_total_level(%)
        #               )
        # ******************************************
        try:
            cloudant_db.validate_resilience_object(resiliencia_from_request)
            # Save/Update community in SQL database
            sql_db.insert_community(community)
            # Save/Update community in Document database
            updated_percentages = sql_db.get_accomplished_percentages_total_and_stage(
                resiliencia_from_request['RESILIENCIA']['stage'], resiliencia_from_request['RESILIENCIA']['step'])
            print(updated_percentages)
            resiliencia_for_community = dict(
                POBLAC_ID=community['POBLAC_ID'],
                PUEBLO=community['PUEBLO'],
                RESILIENCIA=resiliencia_from_request
            )
            resiliencia_for_community['RESILIENCIA']['RESILIENCIA']['resilience_stage_level'] = float(updated_percentages['Stage'])
            resiliencia_for_community['RESILIENCIA']['RESILIENCIA']['resilience_total_level'] = float(updated_percentages['Total'])
            if '_rev' in resiliencia_from_request:
                resiliencia_for_community['_rev'] = resiliencia_from_request['_rev']
                resiliencia_for_community['_id'] = resiliencia_from_request['_id']
            document_save = cloudant_db.update_document_or_save_if_new(resiliencia_for_community)
            return jsonify(document_save)
        except SchemaError as error:
            return jsonify(dict(Schema_error=repr(error)))
        except ValidationError as error:
            return jsonify(dict(Validation_error=repr(error)))
        except FormatError as error:
            return jsonify(dict(Format_error=repr(error)))


@app.route('/api/towns/provinces', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_provinces():
    provinces = sql_db.select_all_states()
    return jsonify(provinces)


@app.route('/api/towns/<province>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_cities(province):
    cities = sql_db.select_all_cities_by_state(province)
    if not cities:
        cities.append("Provincia no encontrada.")
    return jsonify(cities)


@app.route('/api/towns/<province>/<city>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_towns(province, city):
    towns = sql_db.select_all_towns_by_state_and_city(province, city)
    if not towns:
        towns.append("No se ha encontrado la provincia o el canton.")
    return jsonify(towns)


@app.route('/api/towns/<province>/<city>/<town>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_poblado(province, city, town):
    town = sql_db.select_town_dictionary_by_state_city_and_name(province, city, town)
    if not town:
        town = "Poblado, Canton o Provincia no encontrados."
    return jsonify(town)


# ********************* LISTS *****************************************
# List of Resilience Stages
@app.route('/api/resilience/stages', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_stages():
    stages = sql_db.select_all_stages()
    if not stages:
        stages.append("Error in database.")
    return jsonify(stages)


# List of Resilience Steps
@app.route('/api/resilience/steps', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_steps():
    steps = sql_db.select_all_resilience_steps()
    if not steps:
        steps.append("Error in database.")
    return jsonify(steps)


# List of Resilience indicators
@app.route('/api/resilience/indicators', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_indicators():
    indicators = sql_db.select_all_indicators()
    if not indicators:
        indicators.append("Error in database.")
    return jsonify(indicators)


# *************************** COUNTERS *****************************
# Number of resilience stages
@app.route('/api/resilience/stages_count', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_stages_count():
    stages_count = sql_db.count_resilience_stages()
    if not stages_count:
        stages_count.append("Error in database.")
    stages_count = dict(Stages_count=int(stages_count))
    return jsonify(stages_count)


# Number of resilience steps
@app.route('/api/resilience/steps_count', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_steps_count():
    steps_count = sql_db.count_resilience_steps()
    if not steps_count:
        steps_count.append("Error in database.")
    steps_count = dict(Steps_count=int(steps_count))
    return jsonify(steps_count)


# Number of resilience steps within a given resilience stage
@app.route('/api/resilience/steps_count_within_stage/<stage>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_steps_count_within_stage(stage):
    steps_count_within_stage = sql_db.count_resilience_steps_within_stage(stage)
    if not steps_count_within_stage:
        steps_count_within_stage.append("Error in database.")
    steps_count_within_stage = dict(Steps_count_within_stage=int(steps_count_within_stage))
    return jsonify(steps_count_within_stage)


# Number of resilience steps within a given resilience stage
@app.route('/api/resilience/steps_count_by_stage/', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_steps_count_by_stage():
    steps_count_by_stage = sql_db.get_steps_by_stage()
    if not steps_count_by_stage:
        steps_count_by_stage.append("Error in database.")
    steps_count_by_stage = dict(Steps_count_by_stage=steps_count_by_stage)
    return jsonify(steps_count_by_stage)


# Number of total accomplished resilience steps, this doesn't count the current one
@app.route('/api/resilience/total_accomplished_steps/<current_stage>/<current_step>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_total_accomplished_steps(current_stage, current_step):
    total_accomplished_steps = sql_db.count_accomplished_resilience_steps(current_stage, current_step)
    if not total_accomplished_steps:
        total_accomplished_steps.append("Error in database.")
    total_accomplished_steps = dict(Total_accomplished_steps=int(total_accomplished_steps))
    return jsonify(total_accomplished_steps)


# Number of accomplished resilience steps within a given resilience stage, this doesn't count the current one
@app.route('/api/resilience/accomplished_steps_within_stage/<current_stage>/<current_step>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_accomplished_steps_within_stage(current_stage, current_step):
    accomplished_steps_within_stage = sql_db.count_accomplished_resilience_steps_within_stage(current_stage, current_step)
    if not accomplished_steps_within_stage:
        accomplished_steps_within_stage.append("Error in database.")
    accomplished_steps_within_stage = dict(Accomplished_steps_within_stage=int(accomplished_steps_within_stage))
    return jsonify(accomplished_steps_within_stage)


# Percentages of accomplished resilience steps, total and within stage, this doesn't count the current step
@app.route('/api/resilience/accomplished_percentages/<current_stage>/<current_step>', methods=['GET'])
@cross_origin(send_wildcard=True)
def get_accomplished_percentages(current_stage, current_step):
    accomplished_percentages = sql_db.get_accomplished_percentages_total_and_stage(current_stage, current_step)
    if not accomplished_percentages:
        accomplished_percentages.append("Error in database.")
    else:
        accomplished_percentages['Total'] = float(accomplished_percentages['Total'])
        accomplished_percentages['Stage'] = float(accomplished_percentages['Stage'])
    return jsonify(accomplished_percentages)


# ************************** END OF DATABASE FUNCTIONS ***************************

@atexit.register
def shutdown():
    if client:
        client.disconnect()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
