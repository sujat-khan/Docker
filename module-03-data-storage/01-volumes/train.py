"""train.py — Train a scikit-learn model and save to the mounted volume."""
import pickle
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("Training RandomForestClassifier...")

# Load the classic Iris dataset
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print(f"Test accuracy: {acc:.4f}")

# Save to /app/models (which should be a mounted volume)
os.makedirs("/app/models", exist_ok=True)
model_path = "/app/models/iris_model.pkl"

with open(model_path, "wb") as f:
    pickle.dump({"model": model, "classes": load_iris().target_names.tolist()}, f)

print(f"Model saved to {model_path}")
print(f"File size: {os.path.getsize(model_path) / 1024:.1f} KB")
print()
print("The container will exit now.")
print("But the model lives on in the Docker volume!")
