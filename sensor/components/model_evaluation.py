from sensor.entity.config_entity import  ModelEvaluationConfig
from sensor.entity.artifact_entity import ModelEvaluationArtifact,DataValidationArtifact,ModelTrainerArtifact
from sensor.constant.training_pipeline import TARGET_CLASS
from sensor.ml.model.estimator import Target_value_mapping,ModelResolver
from sensor.exception import SensorException
from sensor.utils.main_utils import load_object
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.logger import logging
import os,sys
import pandas as pd
class ModelEvaluation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                model_evaluation_config:ModelEvaluationConfig,
                model_trainer_artifact:ModelTrainerArtifact) -> None:
        try:
                self.data_validation_artifact=data_validation_artifact
                self.model_evaluation_config=model_evaluation_config
                self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise SensorException(e)

    def initiate_model_evaluation(self):
        try:
            valid_train_file_path=self.data_validation_artifact.valid_train_file_path
            valid_test_file_path=self.data_validation_artifact.valid_test_file_path
            
            valid_train_df=pd.read_csv(valid_train_file_path)
            valid_test_df=pd.read_csv(valid_test_file_path)

            df=pd.concat([valid_train_df,valid_test_df])
            y_true=df[TARGET_CLASS]
            y_true.replace(Target_value_mapping().to_dict(),inplace=True)
            df.drop(TARGET_CLASS,axis=1,inplace=True)

            train_model_file_path=self.model_trainer_artifact.trained_model_file_path
            model_revsolver=ModelResolver()
            is_model_accepted=True

            if not model_revsolver.is_exists():
                model_evaluator_artifact=ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    trained_model_file_path=train_model_file_path,
                    best_model_file_path=None,
                    changed_accuracy=None,
                    best_model_metric_artifact=None,
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact
                )
                logging.info(f"Model Evaluation Artifact{model_evaluator_artifact} ")
                return model_evaluator_artifact
            
            latest_model_path=model_revsolver.get_best_model_path()
            
            latest_model=load_object(file_path=latest_model_path)
            trained_model=load_object(file_path=train_model_file_path)

            y_trained_pred=trained_model.predict(df)
            y_latest_pred=latest_model.predict(df)

            trained_metric=get_classification_score(y_true,y_trained_pred)
            latest_metric=get_classification_score(y_true,y_latest_pred)

            improved_accuracy=trained_metric.f1_score-latest_metric.f1_score

            if self.model_evaluation_config.model_evaluation_threshold < improved_accuracy:
                is_model_accepted=True
            else:
                is_model_accepted=False

            model_evaluator_artifact=ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                trained_model_file_path=train_model_file_path,
                best_model_file_path=latest_model_path,
                changed_accuracy=improved_accuracy,
                best_model_metric_artifact=latest_metric,
                train_model_metric_artifact=trained_metric
            )

            logging.info(f"Model Evaluation Artifact{model_evaluator_artifact} ")
            return model_evaluator_artifact
        except Exception as e:
            raise SensorException(e,sys)


