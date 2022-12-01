from sensor.exception import SensorException
import os,sys
from sensor.pipeline.training_pipeline import TrainingPipeline
from fastapi import FastAPI
from fastapi.responses import Response
from sensor.utils.main_utils import load_object
from sensor.ml.model.estimator import ModelResolver,Target_value_mapping
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.constant.application import APP_HOST,APP_PORT
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run



app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        pipeline=TrainingPipeline()
        if pipeline.is_pipeline_running:
            return Response("Training pipeline is running")
        pipeline.run_pipeline()
        return Response("Training Successful !")
    except Exception as e:
        return Response(f"error occured {e} ")



@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe

        df=None
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(Target_value_mapping().reverse_mapping(),inplace=True)

        #decide how to return file to user
    except Exception as e:
        raise Response(f"Error Occured! {e}")



if __name__=='__main__':
    app_run(app,host=APP_HOST,port=APP_PORT)

    