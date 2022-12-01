from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
from sensor.exception import SensorException
import os,sys
import shutil


class Model_Pusher:
    def __init__ (self,model_pusher_config:ModelPusherConfig,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            self.model_pusher_config=model_pusher_config
            self.mode_evaluation_artifact=model_evaluation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            trained_model_path=self.mode_evaluation_artifact.trained_model_file_path

            #saving the trained model to model pusher directory
            model_file_path=self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=model_file_path)

            #saving the model to saved directory
            saved_file_path=self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=saved_file_path)

            model_pusher_artifact=ModelPusherArtifact(saved_model_path=saved_file_path,model_file_path=model_file_path)
            return model_pusher_artifact
            
        except Exception as e:
            raise SensorException(e,sys)
