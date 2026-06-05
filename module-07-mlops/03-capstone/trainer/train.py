"""
train.py — Capstone training script.
Trains an Iris classifier and logs everything to MLflow.
"""
import argparse
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score

parser = argparse.ArgumentParser()
parser.add_argument("--n-estimators", type=int, default=100)
parser.add_argument("--max-depth", type=int, default=5)
parser.add_argument("--model", choices=["rf", "logistic"], default="rf")
args = parser.parse_args()

# Load data
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("iris-classification")

with mlflow.start_run(run_name=f"{args.model}-n{args.n_estimators}-depth{args.max_depth}"):

    # Build model
    if args.model == "rf":
        model = RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
        params = {"model_type": "random_forest", "n_estimators": args.n_estimators, "max_depth": args.max_depth}
    else:
        model = LogisticRegression(max_iter=1000, random_state=42)
        params = {"model_type": "logistic_regression"}

    mlflow.log_params(params)

    # Train
    model.fit(X_train, y_train)

    # Metrics
    preds = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "f1_weighted": f1_score(y_test, preds, average="weighted"),
        "cv_accuracy": np.mean(cross_val_score(model, X, y, cv=5)),
    }
    mlflow.log_metrics(metrics)

    for k, v in metrics.items():
        print(f"  {k:<15}: {v:.4f}")

    # Log model to MLflow registry
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="IrisClassifier",
        input_example=X_train[:3],
    )
    print("Model logged to MLflow ✅")
