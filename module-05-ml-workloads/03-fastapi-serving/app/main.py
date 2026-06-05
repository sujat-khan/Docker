"""FastAPI ML serving API."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import pickle
import numpy as np
import os

model_data = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_data
    path = os.getenv("MODEL_PATH", "models/iris_model.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            model_data = pickle.load(f)
        print(f"✅ Model loaded from {path}")
    else:
        print(f"⚠️ No model found at {path}. /predict will return 503.")
    yield


app = FastAPI(
    title="Iris Classifier API",
    description="Scikit-learn model served via FastAPI inside Docker",
    version="1.0.0",
    lifespan=lifespan,
)


class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., example=5.1, ge=0, description="Sepal length in cm")
    sepal_width: float = Field(..., example=3.5, ge=0, description="Sepal width in cm")
    petal_length: float = Field(..., example=1.4, ge=0, description="Petal length in cm")
    petal_width: float = Field(..., example=0.2, ge=0, description="Petal width in cm")


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict


@app.get("/")
def root():
    return {"service": "Iris Classifier API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model_data is not None}


@app.get("/model-info")
def model_info():
    if model_data is None:
        raise HTTPException(503, "Model not loaded")
    return {
        "model_type": type(model_data["model"]).__name__,
        "classes": model_data["classes"],
        "features": model_data["features"],
        "training_accuracy": model_data.get("accuracy"),
        "params": model_data.get("params"),
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures):
    if model_data is None:
        raise HTTPException(503, "Model not loaded. Train first.")

    X = np.array([[features.sepal_length, features.sepal_width,
                   features.petal_length, features.petal_width]])

    model = model_data["model"]
    classes = model_data["classes"]

    proba = model.predict_proba(X)[0]
    pred_idx = int(np.argmax(proba))

    return PredictionResponse(
        prediction=classes[pred_idx],
        confidence=float(proba[pred_idx]),
        probabilities={c: float(p) for c, p in zip(classes, proba)},
    )
