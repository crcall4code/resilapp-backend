# -*- coding: latin_1 -*-
from sqlalchemy import Text, Float, Integer, MetaData, create_engine, Table, Column, insert, select, and_, distinct, \
    update
from sqlalchemy.sql import func
from json import dumps
from pprint import pprint


class Db2Database:
    __instance = None

    @staticmethod
    def get_instance():
        if Db2Database.__instance is None:
            Db2Database()
        return Db2Database.__instance

    def __init__(self):
        if Db2Database.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            Db2Database.__instance = self
            self.username = "mhg98374"
            self.password = "b7gqx63^51fnrqvp"
            self.host = "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net"
            self.port = 50000
            self.schema = "BLUDB"  # "LFJ47179"
            self.db2ConnectionString = "db2+ibm_db://{}:{}@{}:{}/{}".format(self.username, self.password, self.host,
                                                                            self.port, self.schema)
            self.engine = create_engine(self.db2ConnectionString, pool_size=1, max_overflow=0)
            self.mainConnection = self.engine.connect()
            self.metadata = MetaData()
            self.Towns = Table('POBLADOS', self.metadata,
                               Column('OBJECTID', Integer(), nullable=False, unique=True, primary_key=True),
                               Column('POBLAC_ID', Integer(), nullable=False),
                               Column('PROVINCIA', Text(), nullable=False),
                               Column('CANTON', Text(), nullable=False),
                               Column('PUEBLO', Text(), nullable=False),
                               Column('X_COORDENATES', Float(), nullable=False),
                               Column('Y_COORDENATES', Float(), nullable=False)
                               )
            self.Communities = Table('COMMUNITIES', self.metadata,
                                     Column('POBLAC_ID', Integer(), nullable=False),
                                     Column('PUEBLO', Text(), nullable=False),
                                     Column('VER', Text(), nullable=True)
                                     )
            self.Resiliencia = Table('RESILIENCIA-PASOS', self.metadata,
                                     Column('ID', Integer(), nullable=False, unique=True, primary_key=True),
                                     Column('Etapa', Integer(), nullable=False),
                                     Column('Paso', Integer(), nullable=False),
                                     Column('Detalle', Text(), nullable=False),
                                     Column('Referencia', Text(), nullable=True),
                                     Column('INDICADOR', Text(), nullable=True),
                                     Column('VERIFICADOR', Text(), nullable=True),
                                     Column('DESCRIPCION', Text(), nullable=True)
                                     )

# ****************************** TOWNS FUNCTIONS *****************************************
    def select_all_towns(self):
        select_query = select([self.Towns])
        results_proxy = self.mainConnection.execute(select_query)
        towns_names = []
        results = results_proxy.fetchall()
        for row in results:
            # town_city_state = "({},{},{})".format(row[4].replace("\u00c3\u2018","Ñ"),row[3].replace
            # ("\u00c3\u2018","Ñ"),row[2])
            # town_city_state = "({},{},{})".format(row[4].replace("Ã‘","Ñ"),row[3].replace("Ã‘","Ñ"),row[2])
            town_city_state = "({},{},{})".format(row[4], row[3], row[2])
            towns_names.append(town_city_state)
        results_proxy.close()
        return towns_names

    def select_all_states(self):
        select_query = select([self.Towns.c.PROVINCIA]).distinct()
        results_proxy = self.mainConnection.execute(select_query)
        states = results_proxy.fetchall()
        states = [state[0] for state in states]
        results_proxy.close()
        return states

    def select_all_cities_by_state(self, State):
        select_query = select([self.Towns.c.CANTON]).distinct().where(self.Towns.c.PROVINCIA == State)
        print(select_query)
        results_proxy = self.mainConnection.execute(select_query)
        cities = results_proxy.fetchall()
        # cities = [city[0].replace("\u00c3\u2018","Ñ") for city in cities]
        # cities = [city[0].replace("Ã‘","Ñ") for city in cities]
        cities = [city[0] for city in cities]
        results_proxy.close()
        return cities

    def select_all_towns_by_state_and_city(self, State, City):
        select_query = select([self.Towns.c.PUEBLO]).where(
            and_(
                self.Towns.c.PROVINCIA == State,
                # self.towns.c.CANTON==city.replace("Ñ","\u00c3\u2018")
                # self.towns.c.CANTON==city.replace("Ñ","Ã‘")
                self.Towns.c.CANTON == City
            )
        )
        results_proxy = self.mainConnection.execute(select_query)
        towns = results_proxy.fetchall()
        # towns = [town[0].replace("\u00c3\u2018","Ñ") for town in towns]
        # towns = [town[0].replace("Ã‘","Ñ") for town in towns]
        towns = [town[0] for town in towns]
        results_proxy.close()
        return towns

    def select_towns_dictionaries_by_state(self, State):
        select_query = select([self.Towns]).where(self.Towns.c.PROVINCIA == State)
        results_proxy = self.mainConnection.execute(select_query)
        towns = results_proxy.fetchall()
        towns_list = []
        for Town in towns:
            town_as_dictionary = dict(
                # CANTON=Town[3].replace("\u00c3\u2018","Ñ"),
                # PUEBLO=Town[4].replace("\u00c3\u2018","Ñ")
                # CANTON=Town[3].replace("Ã‘","Ñ"),
                # PUEBLO=Town[4].replace("Ã‘","Ñ")
                CANTON=Town[3],
                PUEBLO=Town[4]
            )
            towns_list.append(town_as_dictionary)
        results_proxy.close()
        return towns_list

    def select_towns_dictionaries_by_state_and_city(self, State, City):
        select_query = select([self.Towns]).where(
            and_(
                self.Towns.c.PROVINCIA == State,
                # self.Towns.c.CANTON==city.replace("Ñ","\u00c3\u2018")
                # self.Towns.c.CANTON==city.replace("Ñ","Ã‘")
                self.Towns.c.CANTON == City
            )
        )
        results_proxy = self.mainConnection.execute(select_query)
        towns = results_proxy.fetchall()
        towns_list = []
        for Town in towns:
            town_as_dictionary = dict(
                # PUEBLO=Town[4].replace("\u00c3\u2018","Ñ")
                # PUEBLO=Town[4].replace("Ã‘","Ñ")
                PUEBLO=Town[4]
            )
            towns_list.append(town_as_dictionary)
        results_proxy.close()
        return towns_list

    def select_town_dictionary_by_state_city_and_name(self, state, city, town):
        select_query = select([self.Towns]).where(
            and_(
                self.Towns.c.PROVINCIA == state,
                # self.Towns.c.CANTON==city.replace("Ñ","\u00c3\u2018"),
                # self.Towns.c.PUEBLO==town.replace("Ñ","\u00c3\u2018")
                # self.Towns.c.CANTON==city.replace("Ñ","Ã‘"),
                # self.Towns.c.PUEBLO==town.replace("Ñ","Ã‘")
                self.Towns.c.CANTON == city,
                self.Towns.c.PUEBLO == town
            )
        )
        results_proxy = self.mainConnection.execute(select_query)
        town = results_proxy.fetchone()
        if town is not None:
            town_as_dictionary = dict(
                ID=town[0],
                POBLAC_ID=town[1],
                PROVINCIA=town[2],
                CANTON=town[3],
                PUEBLO=town[4],
                X_COORDENATES=town[5],
                Y_COORDENATES=town[6]
            )
        else:
            town_as_dictionary = dict(Data="Town not found.")
        results_proxy.close()
        return town_as_dictionary

# ************************* COMMUNITIES FUNCTIONS **************************************
    def insert_community(self, community_data_as_dictionary):
        if not self.is_community_in_database(community_data_as_dictionary)[0]:
            insert_statement = self.Communities.insert().values(
                POBLAC_ID=community_data_as_dictionary["POBLAC_ID"],
                PUEBLO=community_data_as_dictionary["PUEBLO"]
            )
            insert_statement.compile().params
            result = self.mainConnection.execute(insert_statement)
            insert_message = "Community added to database."
        else:
            self.update_community(community_data_as_dictionary)
            insert_message = "Community in database updated."
        return insert_message

    def is_community_in_database(self, community_data_as_dictionary):
        is_community_in_db = False
        community = None
        response = [is_community_in_db, community]
        select_query = select([self.Communities]).where(
            self.Communities.c.POBLAC_ID == community_data_as_dictionary["POBLAC_ID"])
        results_proxy = self.mainConnection.execute(select_query)
        community = results_proxy.fetchone()
        if community is not None:
            is_community_in_db = True
            response = [is_community_in_db, community[0]]
        return response

    def update_community(self, CommunityDataAsDictionary):
        update_statement = self.Communities.update().where(
            self.Communities.c.POBLAC_ID == CommunityDataAsDictionary["POBLAC_ID"]).values(
            POBLAC_ID=CommunityDataAsDictionary["POBLAC_ID"],
            PUEBLO=CommunityDataAsDictionary["PUEBLO"]
        )
        update_statement.compile().params
        result = self.mainConnection.execute(update_statement)
        return result

    def select_community_by_poblac_id(self, poblac_id):
        select_query = select([self.Communities]).where(self.Communities.c.POBLAC_ID == poblac_id)
        results_proxy = self.mainConnection.execute(select_query)
        community = results_proxy.fetchone()
        results_proxy.close()
        return community  # tuple

    def select_community_dictionary_by_poblac_id(self, poblac_id):
        select_query = select([self.Communities]).where(self.Communities.c.POBLAC_ID == poblac_id)
        results_proxy = self.mainConnection.execute(select_query)
        community = results_proxy.fetchone()
        community_as_dictionary = dict(
            POBLAC_ID=community[0],
            PUEBLO=community[1],
            RESILIENCIA=community[2]
        )
        results_proxy.close()
        return community_as_dictionary

    def select_community_dictionary_by_state_city_and_name(self, state, city, community_name):
        town = self.select_Town_dictionary_by_State_City_and_Name(state, city, community_name)
        community = self.select_community_dictionary_by_poblac_id(town['POBLAC_ID'])
        return community

# ***************************** RESILIENCE FUNCTIONS ******************************
    def select_all_resilience_steps(self):
        select_query = select([self.Resiliencia]).order_by(
                                                            self.Resiliencia.c.Etapa.asc()
                                                            )
        results_proxy = self.mainConnection.execute(select_query)
        resilience_steps = results_proxy.fetchall()
        # Clean list to get rid of Stage id, titles, references, achievements
        # Stage,step,detail
        resilience_steps = [[step[1], step[2], step[3]] for step in resilience_steps if
                            step[2] != 0]  # Stage,step,detail
        results_proxy.close()
        return resilience_steps

    def select_all_stages(self):
        # Query only registers where Step equals zero --> step zero equals stage title
        select_query = select([self.Resiliencia]).where(self.Resiliencia.c.Paso == 0)
        results_proxy = self.mainConnection.execute(select_query)
        stages = results_proxy.fetchall()
        stages = [[stage[1], stage[3]] for stage in stages]  # stage number, stage name
        results_proxy.close()
        return stages

    def select_all_indicators(self):
        select_query = select([self.Resiliencia]).where(
                                                        self.Resiliencia.c.INDICADOR != None
                                                        ).order_by(
                                                                    self.Resiliencia.c.Etapa.asc()
                                                                    )
        results_proxy = self.mainConnection.execute(select_query)
        indicators = results_proxy.fetchall()
        indicators = [dict(
            Etapa=indicator[1],
            Paso=indicator[2],
            Indicador=indicator[5],
            Verificador=indicator[6],
            Descripcion=indicator[7])
            for indicator in indicators]
        results_proxy.close()
        return indicators

# ************** COUNTERS *****************************
    def count_resilience_steps(self):
        select_query = select([func.count(
                                        self.Resiliencia.c.ID
                                        ).label('Pasos')]).where(
                                                                self.Resiliencia.c.Paso > 0
                                                                )
        results_proxy = self.mainConnection.execute(select_query)
        record = results_proxy.first()
        return record.Pasos

    def count_resilience_steps_within_stage(self, stage):
        select_query = select([func.count(self.Resiliencia.c.ID).label('Pasos')]).where(
            and_(
                self.Resiliencia.c.Etapa == stage,
                self.Resiliencia.c.Paso > 0
            )
        )
        results_proxy = self.mainConnection.execute(select_query)
        record = results_proxy.first()
        return record.Pasos

    def count_resilience_stages(self):
        select_query = select([func.count(self.Resiliencia.c.ID).label('Etapas')]).where(self.Resiliencia.c.Paso == 0)
        results_proxy = self.mainConnection.execute(select_query)
        record = results_proxy.first()
        return record.Etapas

    def count_accomplished_resilience_steps(self, stage, step):
        select_query = select([func.count(self.Resiliencia.c.ID).label('Pasos')]).where(
            and_(
                self.Resiliencia.c.Etapa < stage,
                self.Resiliencia.c.Paso > 0
            )
        )
        results_proxy = self.mainConnection.execute(select_query)
        record = results_proxy.first()
        accomplished_steps = int(record.Pasos) + (int(step)-1)
        return accomplished_steps

    def count_accomplished_resilience_steps_within_stage(self, stage, step):
        select_query = select([func.count(self.Resiliencia.c.ID).label('Pasos')]).where(
            and_(
                self.Resiliencia.c.Etapa == stage,
                self.Resiliencia.c.Paso < step,
                self.Resiliencia.c.Paso > 0
            )
        )
        results_proxy = self.mainConnection.execute(select_query)
        record = results_proxy.first()
        return record.Pasos

    def get_steps_by_stage(self):
        steps_in_stages = {}
        stages = int(self.count_resilience_stages())
        for stage in range(1, stages+1):
            steps = int(self.count_resilience_steps_within_stage(stage))
            steps_in_stages.update({stage:steps})
        return steps_in_stages

    def get_accomplished_percentages_total_and_stage(self, current_stage, current_step):
        total = self.count_accomplished_resilience_steps(current_stage, current_step)
        stage = self.count_accomplished_resilience_steps_within_stage(current_stage, current_step)
        total_count = self.count_resilience_steps()
        stage_count = self.count_resilience_steps_within_stage(current_stage)
        total_percentage = round((total / total_count * 100), 1)
        stage_percentage = round((stage / stage_count * 100), 1)
        percentages = dict(Total=total_percentage, Stage=stage_percentage)
        return percentages


def main():
    db = Db2Database.get_instance()
    pprint(db.get_steps_by_stage())


if __name__ == "__main__":
    main()
