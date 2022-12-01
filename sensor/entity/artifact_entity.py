from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path : str
    test_file_path : str


@dataclass
class DataValidationArtifact:
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    data_validation_status: bool
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str
    
@dataclass
class ClassificationMetricArtifact:
    f1_score:str
    precision_score:str
    recall_score:str

@dataclass
class ModelTrainerArtifact:
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact
    trained_model_file_path:str
    
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool 
    best_model_file_path:str
    trained_model_file_path : str
    changed_accuracy:float
    train_model_metric_artifact:ClassificationMetricArtifact
    best_model_metric_artifact:ClassificationMetricArtifact

@dataclass
class ModelPusherArtifact:
    saved_model_path:str
    model_file_path: str