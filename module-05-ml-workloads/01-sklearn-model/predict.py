"""predict.py — Load saved model and run predictions."""
import pickle
import os
import numpy as np

model_path = "models/iris_model.pkl"
if not os.path.exists(model_path):
    print(f"ERROR: {model_path} not found. Run train.py first.")
    exit(1)

with open(model_path, "rb") as f:
    saved = pickle.load(f)

model = saved["model"]
classes = saved["classes"]
features = saved["features"]

# Get features from environment or use defaults
feature_str = os.getenv("FEATURES", "5.1,3.5,1.4,0.2")
values = [float(x.strip()) for x in feature_str.split(",")]

if len(values) != 4:
    print(f"ERROR: Expected 4 features, got {len(values)}")
    exit(1)

X = np.array([values])
pred_idx = model.predict(X)[0]
proba = model.predict_proba(X)[0]

print(f"\nInput features:")
for name, val in zip(features, values):
    print(f"  {name}: {val}")

print(f"\nPrediction: {classes[pred_idx]}")
print(f"Confidence: {proba[pred_idx]:.2%}")
print(f"\nAll probabilities:")
for cls, prob in zip(classes, proba):
    bar = "█" * int(prob * 30)
    print(f"  {cls:12s} {prob:.2%}  {bar}")
