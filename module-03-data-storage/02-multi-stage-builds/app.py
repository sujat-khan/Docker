"""app.py — simple ML inference script used to compare image sizes."""
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import numpy as np

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

sample = np.array([[5.1, 3.5, 1.4, 0.2]])
pred = model.predict(sample)[0]
proba = model.predict_proba(sample)[0]

class_names = load_iris().target_names
print(f"Prediction: {class_names[pred]}")
print(f"Confidence: {proba[pred]:.2%}")
print("Multi-stage build test: ✅ working!")
