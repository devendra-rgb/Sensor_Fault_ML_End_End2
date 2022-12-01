from  sensor.constant  import training_pipeline
from datetime import datetime
import os

class Training_pipeline_config:
    def __init__(self,timestamp=datetime.now()):
        timestamp:str =timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.training_pipeline_name:str =training_pipeline.PIPELINE_NAME
        self.artifact_dir:str =os.path.join(training_pipeline.ARTIFACT_DIR,timestamp)
        self.timestamp:str =timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:Training_pipeline_config):
        self.data_ingested_dir: str =os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str=os.path.join(
            self.data_ingested_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingested_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME
        )
        self.training_file_path: str= os.path.join(
            self.data_ingested_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME
        )
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_split_ratio: float= training_pipeline.DATA_INGESTION_TEST_TRAIN_SPLIT_RATIO


        
class DataValidationConfig:
    def __init__(self,training_pipeline_config:Training_pipeline_config) :
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALID_DIR_NAME)
        self.data_valid_dir: str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALID_DIR_NAME)
        self.data_invalid_dir : str = os.path.join(self.data_validation_dir,training_pipeline.DATA_INVALID_DIR_NAME)
        self.valid_train_file_path : str= os.path.join(self.data_valid_dir,training_pipeline.VALID_TRAIN_FILE_NAME)
        self.valid_test_file_path : str = os.path.join(self.data_valid_dir,training_pipeline.VALID_TEST_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.data_invalid_dir,training_pipeline.INVALID_TEST_FILE_NAME)
        self.invalid_train_file_path : str = os.path.join(self.data_valid_dir,training_pipeline.INVALID_TRAIN_FILE_NAME)
        self.drift_report_file_path : str = os.path.join(self.data_valid_dir,training_pipeline.DATA_DRIFT_REPORT_DIR_NAME,training_pipeline.DRIFT_FILE_PATH)


class DataTransformationConfig:
    def __init__(self,training_pipeline_config:Training_pipeline_config) -> None:
        self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORM_DIR_NAME)
        self.data_transformed_dir=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMED_DIR_NAME)
        self.transformed_train_file_path=os.path.join(self.data_transformed_dir,training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
        self.transformed_test_file_path=os.path.join(self.data_transformed_dir,training_pipeline.TEST_FILE_NAME.replace("csv","npy"))
        self.transformed_object_file_path=os.path.join(self.data_transformed_dir,training_pipeline.DATA_TRANSFORMED_OBJECT_NAME)
        
class ModelTrainerConfig:
    def __init__(self,training_pipeling_config:Training_pipeline_config) -> None:
        self.model_trainer_dir=os.path.join(training_pipeling_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.model_trained_dir=os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_DIR_NAME)
        self.trained_model_file_path=os.path.join(self.model_trained_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.model_accuracy : float =training_pipeline.MODEL_TRAINER_EXPECTED_ACCURACY_SCORE
        self.overfitting_underfitting_threshold:float=training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD


class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:Training_pipeline_config) -> None:
        self.model_evaluation_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_EVALUATION_DIR_NAME)
        self.model_evalutaion_report_file_path=os.path.join(self.model_evaluation_dir,training_pipeline.MODEL_EVALUATION_REPORT_NAME)
        self.model_evaluation_threshold=training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD

class ModelPusherConfig:
    def __init__(self,training_pipeline_config:Training_pipeline_config):
        self.model_pusher_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_PUSHER_DIR_NAME)
        self.model_file_path=os.path.join(self.model_pusher_dir,training_pipeline.MODEL_FILE_NAME)

        timestamp=round(datetime.now().timestamp())

        self.saved_model_path=os.path.join(training_pipeline.MODEL_PUSHER_SAVED_MODEL,f"{timestamp}",training_pipeline.MODEL_FILE_NAME)
