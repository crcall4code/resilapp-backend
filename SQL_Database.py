# coding=latin_1
from sqlalchemy import Text, Float, Integer, MetaData, create_engine, Table, Column, insert, select, and_, distinct, update
from sqlalchemy.sql import func
from json import dumps
from pprint import pprint

class DB2_Towns:
    __instance = None
    @staticmethod
    def getInstance():
        if DB2_Towns.__instance == None:
            DB2_Towns()
        return DB2_Towns.__instance
    def __init__(self):
        if DB2_Towns.__instance != None:
            raise Exception("This class is a singleton")
        else:
            DB2_Towns.__instance = self
            self.username = "lfj47179"
            self.password = "3hb62wh+7jtbb77n"
            self.host = "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net"
            self.port = 50000
            self.schema = "BLUDB"#"LFJ47179"
            self.db2ConnectionString = "db2+ibm_db://{}:{}@{}:{}/{}".format(self.username, self.password, self.host, self.port, self.schema)
            self.engine = create_engine(self.db2ConnectionString,pool_size=1, max_overflow=0)
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


    def select_all_Towns(self):
        selectQuery = select([self.Towns])
        resultsProxy = self.mainConnection.execute(selectQuery)
        TownsNames = []
        results = resultsProxy.fetchall()
        for row in results:
            Town_City_State = "({},{},{})".format(row[4].replace("\u00c3\u2018","Ñ"),row[3].replace("\u00c3\u2018","Ñ"),row[2])
            TownsNames.append(Town_City_State)
        resultsProxy.close()
        return TownsNames


    def select_all_States(self):
        selectQuery = select([self.Towns.c.PROVINCIA]).distinct()
        resultsProxy = self.mainConnection.execute(selectQuery)
        States = resultsProxy.fetchall()
        States = [state[0] for state in States]
        resultsProxy.close()
        return States


    def select_all_Cities_by_State(self, State):
        selectQuery = select([self.Towns.c.CANTON]).distinct().where(self.Towns.c.PROVINCIA==State)
        print(selectQuery)
        resultsProxy = self.mainConnection.execute(selectQuery)
        Cities = resultsProxy.fetchall()
        Cities = [city[0].replace("\u00c3\u2018","Ñ") for city in Cities]
        #Cities = [city.replace("Ã‘","Ñ") for city in Cities]
        resultsProxy.close()
        return Cities


    def select_all_Towns_by_State_and_City(self, State, City):
        selectQuery = select([self.Towns.c.PUEBLO]).where(
                                                            and_(
                                                                self.Towns.c.PROVINCIA==State,
                                                                self.Towns.c.CANTON==City.replace("Ñ","\u00c3\u2018")
                                                                )
                                                            )
        resultsProxy = self.mainConnection.execute(selectQuery)
        Towns = resultsProxy.fetchall()
        Towns = [town[0].replace("\u00c3\u2018","Ñ") for town in Towns]
        #Towns = [town[0].replace("Ã‘","Ñ") for town in Towns]
        resultsProxy.close()
        return Towns


    def select_Towns_dictionaries_by_State(self, State):
        selectQuery = select([self.Towns]).where(self.Towns.c.PROVINCIA==State)
        resultsProxy = self.mainConnection.execute(selectQuery)
        Towns = resultsProxy.fetchall()
        TownsList = []
        for Town in Towns:
            TownAsDictionary = dict(
                CANTON=Town[3].replace("\u00c3\u2018","Ñ"),
                PUEBLO=Town[4].replace("\u00c3\u2018","Ñ")
                )
            TownsList.append(TownAsDictionary)
        resultsProxy.close()
        return TownsList


    def select_Towns_dictionaries_by_State_and_City(self, State, City):
        selectQuery = select([self.Towns]).where(
                        and_(
                            self.Towns.c.PROVINCIA==State,
                            self.Towns.c.CANTON==City.replace("Ñ","\u00c3\u2018")
                            )
                        )
        resultsProxy = self.mainConnection.execute(selectQuery)
        Towns = resultsProxy.fetchall()
        TownsList = []
        for Town in Towns:
            TownAsDictionary = dict(
                PUEBLO=Town[4].replace("\u00c3\u2018","Ñ")
                )
            TownsList.append(TownAsDictionary)
        resultsProxy.close()
        return TownsList


    def select_Town_dictionary_by_State_City_and_Name(self, State, City, Town):
        selectQuery = select([self.Towns]).where(
                        and_(
                            self.Towns.c.PROVINCIA==State,
                            self.Towns.c.CANTON==City.replace("Ñ","\u00c3\u2018"),
                            self.Towns.c.PUEBLO==Town.replace("Ñ","\u00c3\u2018")
                            )
                        )
        resultsProxy = self.mainConnection.execute(selectQuery)
        Town = resultsProxy.fetchone()
        if Town!= None:
            TownAsDictionary = dict(
                ID=Town[0],
                POBLAC_ID=Town[1],
                PROVINCIA=Town[2],
                CANTON=Town[3].replace("\u00c3\u2018","Ñ"),
                PUEBLO=Town[4].replace("\u00c3\u2018","Ñ"),
                X_COORDENATES=Town[5],
                Y_COORDENATES=Town[6]
                )
        else:
            TownAsDictionary=dict(Data="Town not found.")
        resultsProxy.close()
        return TownAsDictionary

class DB2_Communities:
    __instance = None
    @staticmethod
    def getInstance():
        if DB2_Communities.__instance == None:
            DB2_Communities()
        return DB2_Communities.__instance
    def __init__(self):
        if DB2_Communities.__instance != None:
            raise Exception("This class is a singleton")
        else:
            DB2_Communities.__instance = self
            self.username = "lfj47179"
            self.password = "3hb62wh+7jtbb77n"
            self.host = "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net"
            self.port = 50000
            self.schema = "BLUDB"#"LFJ47179"
            self.db2ConnectionString = "db2+ibm_db://{}:{}@{}:{}/{}".format(self.username, self.password, self.host, self.port, self.schema)
            self.engine = create_engine(self.db2ConnectionString,pool_size=1, max_overflow=0)
            self.mainConnection = self.engine.connect()
            self.metadata = MetaData()
            self.Communities = Table('COMMUNITIES', self.metadata,
                                    Column('POBLAC_ID', Integer(), nullable=False),
                                    Column('PUEBLO', Text(), nullable=False),
                                    Column('RESILIENCIA', Text(), nullable=False)
                                    )


    def insert_Community(self, CommunityDataAsDictionary):
        if (self.is_community_in_database(CommunityDataAsDictionary)[0]==False):
            insert = self.Communities.insert().values(
                POBLAC_ID = CommunityDataAsDictionary["POBLAC_ID"],
                PUEBLO = CommunityDataAsDictionary["PUEBLO"],
                RESILIENCIA = str(CommunityDataAsDictionary["RESILIENCIA"])
            )
            insert.compile().params
            result = self.mainConnection.execute(insert)
            insertMessage = "Community added to database."
        else:
            self.update_Community(CommunityDataAsDictionary)
            insertMessage = "Community in database updated."
        return insertMessage


    def is_community_in_database(self, CommunityDataAsDictionary):
        isCommunityInDB = False
        selectQuery = select([self.Communities]).where(
                                                       and_(
                                                            self.Communities.c.POBLAC_ID==CommunityDataAsDictionary["POBLAC_ID"],
                                                            self.Communities.c.PUEBLO==CommunityDataAsDictionary["PUEBLO"].replace("Ñ","\u00c3\u2018")
                                                            )
                                                       )
        resultsProxy = self.mainConnection.execute(selectQuery)
        community = resultsProxy.fetchone()
        if (community!=None):
            isCommunityInDB = True
        return [isCommunityInDB,community[0]]

    def update_Community(self, CommunityDataAsDictionary):
        update = self.Communities.update().where(
                                                 and_(
                                                      self.Communities.c.POBLAC_ID==CommunityDataAsDictionary["POBLAC_ID"],
                                                      self.Communities.c.PUEBLO==CommunityDataAsDictionary["PUEBLO"].replace("Ñ","\u00c3\u2018")
                                                      )
                                                 ).values(
                                                          POBLAC_ID = CommunityDataAsDictionary["POBLAC_ID"],
                                                          PUEBLO = CommunityDataAsDictionary["PUEBLO"],
                                                          RESILIENCIA = CommunityDataAsDictionary["RESILIENCIA"]
                                                          )
        update.compile().params
        result = self.mainConnection.execute(update)


    def set_Community_Resilience(self, CommunityDataAsDictionary):
        update = self.Communities.update().where(
                                                 and_(
                                                      self.Communities.c.POBLAC_ID==Poblac_ID,
                                                      self.Communities.c.PUEBLO==Town.replace("Ñ","\u00c3\u2018")
                                                      )
                                                 ).values(
                                                          RESILIENCIA = CommunityDataAsDictionary["RESILIENCIA"]
                                                          )
        update.compile().params
        result = self.mainConnection.execute(update)


    def select_community_by_Poblac_ID(self, Poblac_ID):
        selectQuery = select([self.Communities]).where(self.Communities.c.POBLAC_ID==Poblac_ID)
        resultsProxy = self.mainConnection.execute(selectQuery)
        community = resultsProxy.fetchone()
        resultsProxy.close()
        return community #tuple

    def select_community_Dictionary_by_Poblac_ID(self, Poblac_ID):
        selectQuery = select([self.Communities]).where(self.Communities.c.POBLAC_ID==Poblac_ID)
        resultsProxy = self.mainConnection.execute(selectQuery)
        Community = resultsProxy.fetchone()
        CommunityAsDictionary = dict(
            POBLAC_ID=Community[0],
            PUEBLO=Community[1].replace("\u00c3\u2018","Ñ"),
            RESILIENCIA=Community[2]
            )
        resultsProxy.close()
        return CommunityAsDictionary

    def select_community_dictionary_by_state_city_and_name(self, State, City, CommunityName):
        TownsDB = DB2_Towns.getInstance()
        Town = TownsDB.select_Town_dictionary_by_State_City_and_Name(State, City.replace("Ñ","\u00c3\u2018"), CommunityName.replace("Ñ","\u00c3\u2018"))
        Community = self.select_community_Dictionary_by_Poblac_ID(Town['POBLAC_ID'])
        return Community


class DB2_Resilience_Steps:
    __instance = None
    @staticmethod
    def getInstance():
        if DB2_Resilience_Steps.__instance == None:
            DB2_Resilience_Steps()
        return DB2_Resilience_Steps.__instance
    def __init__(self):
        if DB2_Resilience_Steps.__instance != None:
            raise Exception("This class is a singleton")
        else:
            DB2_Resilience_Steps.__instance = self
            self.username = "lfj47179"
            self.password = "3hb62wh+7jtbb77n"
            self.host = "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net"
            self.port = 50000
            self.schema = "BLUDB"#"LFJ47179"
            self.db2ConnectionString = "db2+ibm_db://{}:{}@{}:{}/{}".format(self.username, self.password, self.host, self.port, self.schema)
            self.engine = create_engine(self.db2ConnectionString,pool_size=1, max_overflow=0)
            self.mainConnection = self.engine.connect()
            self.metadata = MetaData()
            self.Resiliencia = Table('RESILIENCIA-PASOS', self.metadata,
                                    Column('ID', Integer(), nullable=False, unique=True, primary_key=True),
                                    Column('Etapa', Integer(), nullable=False),
                                    Column('Paso', Integer(), nullable=False),
                                    Column('Detalle', Text(), nullable=False),
                                    Column('Referencia', Text(), nullable=True),
                                    Column('Logros', Text(), nullable=True),
                                    )


    def select_all_Resilience_steps(self):
        selectQuery = select([self.Resiliencia])
        resultsProxy = self.mainConnection.execute(selectQuery)
        Resilience_steps = resultsProxy.fetchall()
        #Clean list to get rid of Stage id, titles, references, achievments
        Resilience_steps = [[step[1].replace("\u00c3\u2018","Ñ"),step[2].replace("\u00c3\u2018","Ñ"),step[3].replace("\u00c3\u2018","Ñ")] for step in Resilience_steps if step[2]!=0] #Stage,step,detail
        resultsProxy.close()
        return Resilience_steps


    def select_all_Stages(self):
        #Query only registers where Step equals zero --> step zero equals stage title
        selectQuery = select([self.Resiliencia]).where(self.Resiliencia.c.Paso==0)
        resultsProxy = self.mainConnection.execute(selectQuery)
        Stages = resultsProxy.fetchall()
        Stages = [[stage[1].replace("\u00c3\u2018","Ñ"),stage[3].replace("\u00c3\u2018","Ñ")] for stage in Stages] #stage number, stage name
        resultsProxy.close()
        return Stages


    def count_resilience_steps(self):
        selectQuery = select([func.count(self.Resiliencia.c.ID).label('Pasos')]).where(self.Resiliencia.c.Paso>0)
        resultsProxy = self.mainConnection.execute(selectQuery)
        record = resultsProxy.first()
        return record.Pasos


    def count_resilience_steps_within_stage(self, stage):
        selectQuery = select([func.count(self.Resiliencia.c.ID).label('Pasos')]).where(
                                                                                        and_(
                                                                                            self.Resiliencia.c.Etapa==stage,
                                                                                            self.Resiliencia.c.Paso>0
                                                                                        )
                                                                                )
        resultsProxy = self.mainConnection.execute(selectQuery)
        record = resultsProxy.first()
        return record.Pasos


    def count_resilience_stages(self):
        selectQuery = select([func.count(self.Resiliencia.c.ID).label('Etapas')]).where(self.Resiliencia.c.Paso==0)
        resultsProxy = self.mainConnection.execute(selectQuery)
        record = resultsProxy.first()
        return record.Etapas


    def count_accomplished_resilience_steps(self, stage, step):
        selectQuery = select([func.count(self.Resiliencia.c.ID).label('Pasos')]).where(
                                                                                        and_(
                                                                                            self.Resiliencia.c.Etapa<=stage,
                                                                                            self.Resiliencia.c.Paso<step,
                                                                                            self.Resiliencia.c.Paso>0
                                                                                        )
                                                                                )
        resultsProxy = self.mainConnection.execute(selectQuery)
        record = resultsProxy.first()
        return record.Pasos


    def count_accomplished_resilience_steps_within_stage(self, stage, step):
        selectQuery = select([func.count(self.Resiliencia.c.ID).label('Pasos')]).where(
                                                                                        and_(
                                                                                            self.Resiliencia.c.Etapa==stage,
                                                                                            self.Resiliencia.c.Paso<step,
                                                                                            self.Resiliencia.c.Paso>0
                                                                                        )
                                                                                )
        resultsProxy = self.mainConnection.execute(selectQuery)
        record = resultsProxy.first()
        return record.Pasos


    def get_accomplished_percentages_total_and_stage(self, CurrentStage, CurrentStep):
        Total = self.count_accomplished_resilience_steps(CurrentStage, CurrentStep)
        Stage = self.count_accomplished_resilience_steps_within_stage(CurrentStage, CurrentStep)
        TotalCount = self.count_resilience_steps()
        StageCount = self.count_resilience_steps_within_stage(CurrentStage)
        TotalPercentage = round((Total/TotalCount*100),1)
        StagePercentage = round((Stage/StageCount*100),1)
        Percentages = dict(Total=TotalPercentage,Stage=StagePercentage)
        return Percentages


def main():
    db = DB2_Resilience_Steps.getInstance()
    steps = db.count_resilience_steps()
    stages = db.count_resilience_stages()
    accomplished = db.count_accomplished_resilience_steps(2,8)
    accomplished_in = db.count_accomplished_resilience_steps_within_stage(2,8)
    percentages = db.get_accomplished_percentages_total_and_stage(2,8)
    print("Etapas: ", stages)
    print("Pasos: ",steps)
    print("Cumplidos: ",accomplished,"(total) / ", accomplished_in, "(en esta etapa)")
    print("Percentages: ", percentages["Total"], "% / ", percentages["Stage"],"%")



if __name__=="__main__":
    main()
