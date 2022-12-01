from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import Model_Pusher
from sensor.entity.config_entity import Training_pipeline_config,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
import os,sys
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.cloud_storage.s3_sync import S3_Sync
class TrainingPipeline:
    is_pipeline_running=False
    def __init__(self):
        self.training_pipeline_config=Training_pipeline_config()
        self.s3_sync=S3_Sync()
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion ")
            dataingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=dataingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Data Validation ")
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validataion_config=data_validation_config)
            logging.info("Data Validation_initiated")
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            logging.info("Starting Data Transformation ")
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            logging.info("Data Transformation Initiated")
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact)-> ModelTrainerArtifact:

        try:
            model_training_config=ModelTrainerConfig(self.training_pipeline_config)
            logging.info("Model training Configured ")
            model_training=ModelTrainer(model_trainer_config=model_training_config,data_transformation_artifact=data_transformation_artifact)
            logging.info("Model training Initiated")
            model_trainer_artifact=model_training.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_evaluation(self,model_trainer_artifact:ModelTrainerArtifact,data_validation_artifact:DataValidationArtifact)->ModelEvaluationArtifact:
        try:
            model_evaluation_config=ModelEvaluationConfig(self.training_pipeline_config)
            logging.info("Model evaluation Configured ")
            model_evaluation=ModelEvaluation(data_validation_artifact=data_validation_artifact,model_trainer_artifact=model_trainer_artifact,model_evaluation_config=model_evaluation_config)
            logging.info("Model Evaluation Initiated")
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact


        except Exception as e:
            raise SensorException(e,sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config=ModelPusherConfig(self.training_pipeline_config)
            logging.info("Model Pusher configured ")
            model_pusher=Model_Pusher(model_pusher_config=model_pusher_config,model_evaluation_artifact=model_evaluation_artifact)
            logging.info("Model Pusher initated")
            model_pusher_artifact=model_pusher.initiate_model_pusher()
            logging.info(f"model pusher artifact {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3//:{TRAINING_BUCKET_NAME}/artirfact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder_path=self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)
    def sync_saved_model_to_s3(self):
        try:
            aws_bucket_url=f"s3//:{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder_path=SAVED_MODEL_DIR,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)



    def run_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running=True
            data_ingestion_artifact:DataIngestionArtifact=self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact:ModelEvaluationArtifact=self.start_model_evaluation(model_trainer_artifact=model_trainer_artifact,data_validation_artifact=data_validation_artifact)
            if model_evaluation_artifact.is_model_accepted==False:
                raise Exception("Trained model is not better than best model")
            model_pusher_artifact:ModelPusherArtifact=self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            TrainingPipeline.is_pipeline_running=False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_to_s3()
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainingPipeline.is_pipeline_running=False
            raise SensorException(e,sys)
        
        
