from sensor.entity.config_entity import Training_pipeline_config,DataTransformationConfig
from sensor.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek
from sensor.constant.training_pipeline import TARGET_CLASS
from sensor.ml.model.estimator import Target_value_mapping
from sensor.utils.main_utils import save_numpy_array_data,save_object
import numpy as np


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise SensorException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df=pd.read_csv(file_path)
            return df
        except Exception as e:
            SensorException(e,sys)
    
    @classmethod
    def get_data_transformer_object(self)-> Pipeline:
        try:
            roboust_sclar=RobustScaler()
            imputer=SimpleImputer(strategy='constant',fill_value=0)
            preprocessor=Pipeline(
                steps=[
                    ('imputer',imputer),#handle missing values  
                    ('robust_sclar',roboust_sclar)  #keep every feature in same range by handling outliers
                    ]
            )
            return preprocessor
        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")

            #reading_data
            train_file=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_file=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)            
            logging.info("Reading data completed")

            #preprocessor
            preprocessor=DataTransformation.get_data_transformer_object()            
            logging.info("Preprocessor initiated")            

            #training_dataframe
            input_feature_train=train_file.drop([TARGET_CLASS],axis=1)
            target_feature_train=train_file[TARGET_CLASS]
            target_feature_train=target_feature_train.replace(Target_value_mapping().to_dict())

            #test_dataframe
            input_feature_test=test_file.drop(TARGET_CLASS,axis=1)
            target_feature_test=test_file[TARGET_CLASS]
            target_feature_test=target_feature_test.replace(Target_value_mapping().to_dict())

            #preprocessing input to np array
            preprocessor_object=preprocessor.fit(input_feature_train)            
            transformed_input_feature_train=preprocessor_object.transform(input_feature_train)  
            transformed_input_feature_test=preprocessor_object.transform(input_feature_test)          
            logging.info("Preprocessing completed")

            #sampling data

            sm=SMOTETomek(sampling_strategy='minority')

            input_feature_train_final,target_feature_train_final=sm.fit_resample(transformed_input_feature_train,target_feature_train)
            input_feature_test_final,target_feature_test_final=sm.fit_resample(transformed_input_feature_test,target_feature_test)
            logging.info("Sampling completed")

            #converting to array
            train_arr=np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr=np.c_[input_feature_test_final,np.array(target_feature_test_final)]
            logging.info("Converting to array completed")

            #saving numpy array
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=preprocessor_object)

            #Data_trasformation_artifact
            data_transformation_articact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            logging.info(f"Data Transformation Artifact : {data_transformation_articact}")
            return data_transformation_articact


        except Exception as e:
            raise SensorException(e,sys)
    


        