from sensor.configuration.mongodb_connection import MongoDBclient
from sensor.constant.database import DATABASE_NAME
import sys
from typing import Optional
import pandas as pd
import numpy as np
from sensor.exception import SensorException
class SensorData():

    def __init__(self):
        
        try:
            self.mongo_client=MongoDBclient(database_name=DATABASE_NAME)
        
        except Exception as e:
            raise SensorException(e,sys)

    def export_collection_to_dataframe(self,collection_name: str ,database_name:Optional[str] =None) -> pd.DataFrame:
        try:
            """
            exporting entire collection as data frame 
            """
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            
            else:
                collection=self.mongo_client[database_name][collection_name]

            dataframe=pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns.to_list():
                dataframe=dataframe.drop(columns=["_id"],axis=1)
            
            dataframe.replace({"na":np.nan},inplace=True)

            return dataframe

        except Exception as e:
            pass
        