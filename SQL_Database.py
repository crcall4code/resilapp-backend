from sqlalchemy import Text, Float, MetaData, create_engine, Table, Column, insert, select

class DB2:
    def __init__(self):
        self.username = "lfj47179"
        self.password = "3hb62wh+7jtbb77n"
        self.host = "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net"
        self.port = 50000
        self.schema = "BLUDB"    #Schema:"LFJ47179"
        self.engine = create_engine("db2+ibm_db://{}:{}@{}:{}/{}".format(self.username, self.password, self.host, self.port, self.schema))
        self.mainConnection = self.engine.connect()
        self.metadata = MetaData()
        self.Communities = Table('COMMUNITIES', self.metadata,
                                Column('NAME', Text(), nullable=False),
                                Column('UBICATION_X', Float(), nullable=False),
                                Column('UBICATION_Y', Float(), nullable=False),
                                Column('PROVINCE', Text(), nullable=False),
                                Column('CANTON', Text(), nullable=False),
                                Column('RESILIENCE', Text(), nullable=False)
                                )


    def insert(self, DataAsDictionary):
        insert = self.Communities.insert().values(
            NAME =DataAsDictionary["NAME"],
            UBICATION_X =DataAsDictionary["UBICATION_X"],
            UBICATION_Y =DataAsDictionary["UBICATION_Y"],
            PROVINCE =DataAsDictionary["PROVINCE"],
            CANTON =DataAsDictionary["CANTON"],
            RESILIENCE=DataAsDictionary["RESILIENCE"]
        )
        insert.compile().params
        result = self.mainConnection.execute(insert)

    def select(self):
        selectQuery = select([self.Communities]).where(self.Communities.c.NAME!=None)
        resultsProxy = self.mainConnection.execute(selectQuery)
        resultsList = []
        results = resultsProxy.fetchall()
        for row in results:
            community = []
            community.append(row[0]) #Name
            community.append(row[1]) #Ubication_X
            community.append(row[2]) #Ubication_Y
            community.append(row[3]) #Province
            community.append(row[4]) #Canton
            community.append(row[5]) #Resilience
            resultsList.append(community)
        resultsProxy.close()
        return resultsList


def main():
    db = DB2()
    data= dict(
        NAME = "Upala",
        UBICATION_X = -83.123,
        UBICATION_Y = 10.522,
        PROVINCE = "Alajuela",
        CANTON = "Upala",
        RESILIENCE='{"badges":[{"icon": "url_for_image","title": "Beginner","description": "First Badge"},{"icon": "url_for_image","title": "Second Runner","description": "Second Badge"},{"icon": "url_for_image","title": "Third Runner","description": "Third Badge"}],"resilience_level": 0.8}'
        )
    #db.insert(data)
    communities = db.select()
    print(communities)

if __name__=="__main__":
    main()
