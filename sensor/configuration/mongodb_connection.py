import pymongo
from sensor.constant.env_variable import MONGODB_URL_KEY
from sensor.constant.database import DATABASE_NAME
import certifi
import os
from dotenv import load_dotenv
load_dotenv()

ca=certifi.where()

class MongoDBclient:
    client=None
    def __init__(self,database_name=DATABASE_NAME) -> None:

        try:
            if MongoDBclient.client == None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                #print(mongo_db_url)
                if "localhost" in mongo_db_url:
                    MongoDBclient.client=pymongo.MongoClient(mongo_db_url)
                else:
                    MongoDBclient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                self.client=MongoDBclient.client

                self.database=self.client[database_name]

                self.database_name=database_name

        except Exception as e:
            raise e
