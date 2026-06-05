"""train.py — Train and save an Iris classifier."""
import pickle
import os
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Hyperparameters (configurable via environment variables)
n_estimators = int(os.getenv("N_ESTIMATORS", 100))
max_depth = int(os.getenv("MAX_DEPTH", 5))

print(f"Training RandomForest (n_estimators={n_estimators}, max_depth={max_depth})")

# Load and split
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier(
    n_estimators=n_estimators,
    max_depth=max_depth,
    random_state=42,
)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)
print(f"\nTest Accuracy: {accuracy:.4f}")
print(f"\nClassification Report:\n{classification_report(y_test, preds, target_names=iris.target_names)}")

# Save
os.makedirs("models", exist_ok=True)
model_path = "models/iris_model.pkl"
with open(model_path, "wb") as f:
    pickle.dump({
        "model": model,
        "classes": iris.target_names.tolist(),
        "features": iris.feature_names,
        "accuracy": accuracy,
        "params": {"n_estimators": n_estimators, "max_depth": max_depth},
    }, f)

size_kb = os.path.getsize(model_path) / 1024
print(f"\nModel saved to {model_path} ({size_kb:.1f} KB)")
