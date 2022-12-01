from sensor.entity.config_entity import ModelTrainerConfig,Training_pipeline_config
from sensor.entity.artifact_entity import ModelTrainerArtifact,DataValidationArtifact,DataTransformationArtifact
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from sensor.utils.main_utils import load_numpy_array_data,load_object,save_object
from xgboost import XGBClassifier
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact) -> None:
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    

    def train_model(self,X_train,y_train):
        try:
            xgb_clf=XGBClassifier()
            xgb_clf.fit(X_train,y_train)
            return xgb_clf
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            #taking paths of train and test
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            #dividing the array
            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

             #training model
            
            model= self.train_model(X_train,y_train)

            y_train_pred=model.predict(X_train)
            classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

            if classification_train_metric.f1_score <= self.model_trainer_config.model_accuracy:
                raise SensorException("Trained Model accuracy is less than required accuracy",sys)

            #overfitting and underfitting

            y_test_pred=model.predict(X_test)
            classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

            diff=abs(classification_test_metric.f1_score - classification_train_metric.f1_score)

            if diff>self.model_trainer_config.overfitting_underfitting_threshold:
                raise SensorException("Model is not performing good in test set try to do more expermenting")

            #saving the model with the path

            preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_file_path=self.model_trainer_config.trained_model_file_path
            model_dir_name=os.path.dirname(model_file_path)
            os.makedirs(model_dir_name,exist_ok=True)

            sensor_model=SensorModel(preprocessor=preprocessor,model=model)

            save_object(self.model_trainer_config.trained_model_file_path,obj=sensor_model)

            logging.info("Model is trained and saved successfully")

            model_artifact=ModelTrainerArtifact(
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
                trained_model_file_path=self.model_trainer_config.trained_model_file_path
            )
            logging.info(f"trained model artifact {model_artifact}")
            return model_artifact

        except Exception as e:
            raise SensorException(e,sys)