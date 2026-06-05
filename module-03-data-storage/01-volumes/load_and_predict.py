"""load_and_predict.py — Load the saved model and run predictions."""
import pickle
import os
import numpy as np

model_path = "/app/models/iris_model.pkl"

if not os.path.exists(model_path):
    print(f"ERROR: Model not found at {model_path}")
    print("Run train.py first with the volume mounted!")
    exit(1)

# Load model from the volume
print(f"Loading model from {model_path}...")
with open(model_path, "rb") as f:
    saved = pickle.load(f)

model = saved["model"]
classes = saved["classes"]
print(f"Model loaded successfully: {type(model).__name__}")
print(f"Classes: {classes}")
print()

# Run a few predictions
test_samples = [
    [5.1, 3.5, 1.4, 0.2],  # Setosa
    [6.7, 3.0, 5.2, 2.3],  # Virginica
    [5.8, 2.7, 4.1, 1.0],  # Versicolor
]
feature_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

print("Running predictions:")
print("-" * 50)
for sample in test_samples:
    X = np.array([sample])
    pred_idx = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    confidence = proba[pred_idx]
    print(f"Features: {sample}")
    print(f"  → Prediction: {classes[pred_idx]} (confidence: {confidence:.2%})")
    print()
