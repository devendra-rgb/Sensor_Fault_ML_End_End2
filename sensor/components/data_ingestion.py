from sensor.entity.config_entity import DataIngestionConfig
from pandas import DataFrame
import os
from sklearn.model_selection import train_test_split
from sensor.exception import SensorException
import sys
from sensor.data_access.sensor_data import SensorData
from sensor.exception import SensorException
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.logger import logging
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):

        try:
            self.data_ingestion_config=data_ingestion_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            SensorException(e,sys)
    def export_data_into_feature_store(self) -> DataFrame:
        try:
            logging.info("Started Fetching Data... ")
            
            sensordata=SensorData()
            dataframe=sensordata.export_collection_to_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_filepath=self.data_ingestion_config.feature_store_file_path
            

            logging.info(f"making csv file of collection data")
            dir_path=os.path.dirname(feature_store_filepath)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_filepath,index=False,header=True)

            return dataframe
        except Exception as e:
            raise SensorException(e,sys)
            
    def split_data_as_train_test(self,dataframe:DataFrame) -> None:
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_split_ratio)

            train_path=os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(train_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)

            
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe=self.export_data_into_feature_store()
            dataframe=dataframe.drop(self._schema_config['drop_columns'],axis=1)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)


        