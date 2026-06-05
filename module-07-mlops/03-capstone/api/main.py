"""
main.py — Capstone Prediction API.
Loads the Production model from MLflow and serves predictions.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import mlflow.sklearn
import numpy as np
import os

clf = None
class_names = ["setosa", "versicolor", "virginica"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    global clf
    model_name = os.getenv("MODEL_NAME", "IrisClassifier")
    model_stage = os.getenv("MODEL_STAGE", "Production")
    try:
        uri = f"models:/{model_name}/{model_stage}"
        print(f"Loading model from MLflow: {uri}")
        clf = mlflow.sklearn.load_model(uri)
        print("Model loaded ✅")
    except Exception as e:
        print(f"Could not load Production model: {e}")
        print("API will return 503 until a model is promoted to Production.")
    yield


app = FastAPI(title="MLflow Model API", description="Capstone: loads model from MLflow registry", version="1.0.0", lifespan=lifespan)


class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., example=5.1, ge=0)
    sepal_width: float = Field(..., example=3.5, ge=0)
    petal_length: float = Field(..., example=1.4, ge=0)
    petal_width: float = Field(..., example=0.2, ge=0)


@app.get("/health")
def health():
    return {"status": "healthy", "model_ready": clf is not None}


@app.post("/predict")
def predict(features: IrisFeatures):
    if clf is None:
        raise HTTPException(503, "No Production model registered in MLflow yet. Run train.py first.")
    X = np.array([[features.sepal_length, features.sepal_width, features.petal_length, features.petal_width]])
    proba = clf.predict_proba(X)[0]
    pred_idx = int(np.argmax(proba))
    return {
        "prediction": class_names[pred_idx],
        "confidence": float(proba[pred_idx]),
        "probabilities": {c: float(p) for c, p in zip(class_names, proba)},
    }
