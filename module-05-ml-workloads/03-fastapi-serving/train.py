"""train.py — Train and save the Iris model for serving."""
import pickle
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy:.4f}")

os.makedirs("models", exist_ok=True)
with open("models/iris_model.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "classes": iris.target_names.tolist(),
        "features": iris.feature_names,
        "accuracy": accuracy,
        "params": {"n_estimators": 100, "max_depth": 5},
    }, f)
print("Model saved to models/iris_model.pkl")
