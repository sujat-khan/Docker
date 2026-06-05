"""
main.py — FastAPI ML serving app.

Trains a simple model on startup (for demo purposes).
In production, you'd load a pre-trained model from a volume or model registry.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np
import os
import redis
import json
import hashlib
from contextlib import asynccontextmanager
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# ── Global model (loaded at startup) ──────────────────
clf = None
class_names = None
redis_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Train model and connect to Redis when the app starts."""
    global clf, class_names, redis_client

    # Train model
    print("Training model...")
    iris = load_iris()
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(iris.data, iris.target)
    class_names = iris.target_names.tolist()
    print(f"Model trained. Classes: {class_names}")

    # Connect to Redis (optional — app works without it)
    try:
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )
        redis_client.ping()
        print("Redis connected ✅")
    except Exception as e:
        print(f"Redis not available (caching disabled): {e}")
        redis_client = None

    yield  # App runs here

    print("Shutting down...")


app = FastAPI(
    title="Iris ML API",
    description="Scikit-learn model served with FastAPI in Docker Compose",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Schemas ────────────────────────────────────────────
class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., example=5.1, ge=0)
    sepal_width: float = Field(..., example=3.5, ge=0)
    petal_length: float = Field(..., example=1.4, ge=0)
    petal_width: float = Field(..., example=0.2, ge=0)


class PredictionOut(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict
    cached: bool = False


# ── Endpoints ──────────────────────────────────────────
@app.get("/")
def root():
    return {"service": "Iris ML API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_ready": clf is not None,
        "redis_connected": redis_client is not None,
    }


@app.post("/predict", response_model=PredictionOut)
def predict(features: IrisFeatures):
    if clf is None:
        raise HTTPException(503, "Model not ready")

    X = np.array([[features.sepal_length, features.sepal_width,
                   features.petal_length, features.petal_width]])

    # Check Redis cache first
    cache_key = hashlib.md5(str(X.tolist()).encode()).hexdigest()
    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            result = json.loads(cached)
            result["cached"] = True
            return result

    # Run inference
    proba = clf.predict_proba(X)[0]
    pred_idx = int(np.argmax(proba))

    result = {
        "prediction": class_names[pred_idx],
        "confidence": float(proba[pred_idx]),
        "probabilities": {c: float(p) for c, p in zip(class_names, proba)},
        "cached": False,
    }

    # Store in Redis cache (expire after 5 minutes)
    if redis_client:
        redis_client.setex(cache_key, 300, json.dumps(result))

    return result
