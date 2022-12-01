from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.constant import training_pipeline
from sensor.exception import SensorException
from sensor.logger  import logging
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
import os,sys
import pandas as pd
from scipy.stats import ks_2samp


class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validataion_config:DataValidationConfig) -> None:
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validaton_config=data_validataion_config
            self._schema=read_yaml_file(SCHEMA_FILE_PATH)
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_coloumns(self,dataframe:pd.DataFrame) -> bool:
        try:
            no_of_coloumns=len(self._schema['columns'])
            logging.info(f"Required number of coloumns {no_of_coloumns}")
            logging.info(f"Dataframe has coloumns {len(dataframe.columns)}")
            if no_of_coloumns==len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise SensorException(e,sys)
    def validate_numerical_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            numerical_columns=self._schema['numerical_columns']
            data_columns=dataframe.columns

            numerical_columns_present=True
            missing_numerical_columns=[]

            for numerical_column in numerical_columns:
                if numerical_column not in data_columns:
                    missing_numerical_columns.append(numerical_column)
                    numerical_columns_present=False
            
            logging.info(f"missing numerical columns {missing_numerical_columns}")

            return  numerical_columns_present
        except Exception as e:
            raise SensorException(e,sys)
    @staticmethod
    def read_data(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise SensorException(e,sys)
    def detect_data_drift(self,base_data,current_data,threshold=0.05) ->bool:
        try:
            status = True
            report={}
            for column in base_data.columns:
                d1=base_data[column]
                d2=current_data[column]
                is_same_dist=ks_2samp(d1,d2)

                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False

                report.update(

                    {column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":status
                    }}
                )

            #create_directory
            dir_path=os.path.dirname(self.data_validaton_config.drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(self.data_validaton_config.drift_report_file_path,report)

            return status
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Data Validation Fetching started")
            error_message=""
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path


            #reading data from the path
            train_data=DataValidation.read_data(train_file_path)
            test_data=DataValidation.read_data(test_file_path)

            #validate  no of coloumns
            status=self.validate_number_of_coloumns(train_data)
            if not status:
                error_message=f"{error_message}train data does not contain all the coloums\n"

            status=self.validate_number_of_coloumns(test_data)
            if not status:
                error_message=f"{error_message}test data does not contain all the coloumns\n"

            #validate numerical coloumns

            status=self.validate_numerical_columns(train_data)
            if not status:
                error_message=f"{error_message}train data does not contain all the numerical coloums\n"

            status=self.validate_numerical_columns(test_data)
            if not status:
                error_message=f"{error_message}test data does not contain all the numerical coloumns\n"
            
            if len(error_message) >1:
                raise Exception(error_message)
            
            #Data Drift Checking

            status=self.detect_data_drift(base_data=train_data,current_data=test_data)

            data_validation_artifact=DataValidationArtifact(
                data_validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validaton_config.drift_report_file_path,
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)
