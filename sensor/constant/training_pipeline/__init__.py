import os


PIPELINE_NAME="sensor"
ARTIFACT_DIR='artifact'
FILE_NAME='sensor.csv'
TARGET_CLASS="class"
MODEL_FILE_NAME='model.pkl'
SAVED_MODEL_DIR=os.path.join('saved_models')

TEST_FILE_NAME='test.csv'
TRAIN_FILE_NAME='train.csv'

INVALID_TRAIN_FILE_NAME="invalid_train.csv"
INVALID_TEST_FILE_NAME='invalid_test.csv'

VALID_TRAIN_FILE_NAME='valid_train.csv'
VALID_TEST_FILE_NAME='valid_test.csv'

DRIFT_FILE_PATH='drift_report.yaml'
#C:\ineuron\sensor-fault-detection-practice\sensor\config\schema.yaml
SCHEMA_FILE_PATH=os.path.join("sensor","config","schema.yaml")

""" Data Ingestion constanta"""

DATA_INGESTION_COLLECTION_NAME:str ="sensor"
DATA_INGESTION_DIR_NAME:str="data_ingestion" #root directory
DATA_INGESTION_INGESTED_DIR:str ="ingested"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_TEST_TRAIN_SPLIT_RATIO:float =0.2

""" Data Validation Constants """

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALID_DIR_NAME: str = "valid_data"
DATA_INVALID_DIR_NAME: str = "invalid_data"
DATA_DRIFT_REPORT_DIR_NAME: str ="drift_report"

""" Data Transformation Constants """
DATA_TRANSFORM_DIR_NAME :str ="data_transformation"
DATA_TRANSFORMED_DIR_NAME: str = "transformed"
DATA_TRANSFORMED_OBJECT_NAME: str = "transformed_object"

""" Model Trainer Constants """
MODEL_TRAINER_DIR_NAME : str ="model_trainer"
MODEL_TRAINER_TRAINED_DIR_NAME : str ="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME : str="model.pkl"
MODEL_TRAINER_EXPECTED_ACCURACY_SCORE : float =0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD : float =0.05


""" Model Evaluation Constants """
MODEL_EVALUATION_CHANGED_THRESHOLD :float = 0.02
MODEL_EVALUATION_DIR_NAME:str = "model_evaluation"
MODEL_EVALUATION_REPORT_NAME : str= "report.yaml"



""" MOdel Pusher Constants """
MODEL_PUSHER_DIR_NAME='model_pusher'
MODEL_PUSHER_SAVED_MODEL=SAVED_MODEL_DIR