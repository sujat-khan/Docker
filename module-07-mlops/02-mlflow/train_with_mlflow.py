"""
train_with_mlflow.py — Train an Iris classifier and log everything to MLflow.

Run this AFTER starting the MLflow server with: docker compose up -d
Then view results at: http://localhost:5000
"""
import argparse
import mlflow
import mlflow.sklearn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
)
import os
import tempfile

# ── CLI args ────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Train Iris classifier with MLflow tracking")
parser.add_argument("--n-estimators", type=int, default=100)
parser.add_argument("--max-depth", type=int, default=5)
parser.add_argument("--random-state", type=int, default=42)
args = parser.parse_args()

# ── MLflow setup ────────────────────────────────────────
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("iris-classification")

# ── Load data ───────────────────────────────────────────
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=args.random_state, stratify=y
)

# ── Start MLflow run ────────────────────────────────────
run_name = f"rf-n{args.n_estimators}-depth{args.max_depth}"
print(f"\nStarting run: {run_name}")
print(f"Logging to: http://localhost:5000\n")

with mlflow.start_run(run_name=run_name):

    # ── Log parameters ──────────────────────────────────
    params = {
        "n_estimators": args.n_estimators,
        "max_depth": args.max_depth,
        "random_state": args.random_state,
        "model_type": "RandomForestClassifier",
    }
    mlflow.log_params(params)

    # ── Train ───────────────────────────────────────────
    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        random_state=args.random_state,
    )
    model.fit(X_train, y_train)

    # ── Evaluate ────────────────────────────────────────
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="weighted")

    # Cross-validation — log each fold as a step
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv)
    for i, score in enumerate(cv_scores):
        mlflow.log_metric("cv_fold_accuracy", score, step=i)

    # Summary metrics
    metrics = {
        "accuracy": accuracy,
        "f1_weighted": f1,
        "cv_accuracy_mean": float(cv_scores.mean()),
        "cv_accuracy_std": float(cv_scores.std()),
    }
    mlflow.log_metrics(metrics)

    print("Metrics:")
    for k, v in metrics.items():
        print(f"  {k:<22}: {v:.4f}")

    # ── Confusion matrix as artifact ────────────────────
    cm = confusion_matrix(y_test, preds)
    disp = ConfusionMatrixDisplay(cm, display_labels=iris.target_names)
    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, colorbar=False)
    ax.set_title(f"Confusion Matrix — {run_name}")

    with tempfile.TemporaryDirectory() as tmpdir:
        cm_path = os.path.join(tmpdir, "confusion_matrix.png")
        fig.savefig(cm_path, bbox_inches="tight")
        mlflow.log_artifact(cm_path)
    plt.close(fig)

    # ── Log model to registry ───────────────────────────
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="IrisClassifier",
        input_example=X_train[:3],
        signature=mlflow.models.infer_signature(X_train, preds),
    )

    run_id = mlflow.active_run().info.run_id
    print(f"\nRun logged successfully!")
    print(f"View at: http://localhost:5000/#/experiments/1/runs/{run_id}")
