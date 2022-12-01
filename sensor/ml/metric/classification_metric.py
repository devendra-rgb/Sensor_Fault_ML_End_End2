from sensor.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score
import os,sys
from sensor.exception import SensorException
from sensor.logger import logging


def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:

    try:
        logging.info("getting Classification Score ...")
        model_f1_score=f1_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        model_recall_score= recall_score(y_true,y_pred)

        classification_artifact=ClassificationMetricArtifact(f1_score=model_f1_score,precision_score=model_precision_score,recall_score=model_recall_score)
        return classification_artifact
    
    except Exception as e:
        raise SensorException(e,sys)