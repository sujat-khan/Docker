# Lesson 2 — MLflow + Docker for Experiment Tracking

**Module:** MLOps | **Level:** 🏆 Master | **Time:** ~25 min

---

## What You'll Learn
- What MLflow is and what problem it solves
- Run an MLflow tracking server in Docker
- Log experiments, parameters, and metrics from Python
- Compare runs side-by-side in the MLflow UI

---

## The Problem: Tracking ML Experiments

Without a tracking system:
```
Run 1: accuracy=0.87  (what hyperparameters? don't remember)
Run 2: accuracy=0.91  (can't reproduce this — forgot the settings)
Run 3: accuracy=0.89  (which version of data was used?)
```

With MLflow:
```
Every run is logged automatically:
  - Parameters  (n_estimators=100, max_depth=5, ...)
  - Metrics     (accuracy, f1, loss, ...)
  - Artifacts   (model.pkl, plots, confusion matrix)
  - Code version (git commit)
  - Timestamp
```

---

## MLflow Components

| Component | What It Does |
|-----------|-------------|
| **Tracking** | Logs runs, params, metrics — the focus of this lesson |
| **Projects** | Packages code for reproducible runs |
| **Models** | Standardises model packaging |
| **Registry** | Manages model versions and lifecycle (staging → production) |

---

## Step 1 — Start MLflow Tracking Server in Docker

```powershell
cd module-07-mlops\02-mlflow

# Start the MLflow server (stores data locally in ./mlruns)
docker compose up -d

# Check it's running
docker compose ps
```

Open **http://localhost:5000** — you'll see the empty MLflow UI.

---

## Step 2 — Run Your First Tracked Experiment

```powershell
# Install MLflow locally to run the training script
pip install mlflow scikit-learn

# Run the training script — it logs to the Docker MLflow server
python train_with_mlflow.py
```

Refresh **http://localhost:5000** — you'll see the run appear!

Click on the run to see:
- Parameters: `n_estimators`, `max_depth`, `random_state`
- Metrics: `accuracy`, `f1_weighted`, `cv_accuracy`
- Artifacts: `model/` directory

---

## Step 3 — Run More Experiments and Compare

```powershell
# Vary hyperparameters — each run is tracked separately
python train_with_mlflow.py --n-estimators 50 --max-depth 3
python train_with_mlflow.py --n-estimators 200 --max-depth 10
python train_with_mlflow.py --n-estimators 100 --max-depth None
```

Now in the MLflow UI:
1. Select all 4 runs with the checkboxes
2. Click **"Compare"**
3. See a side-by-side metric comparison and parameter table

---

## Step 4 — Register the Best Model

In the MLflow UI:
1. Click on your best run (highest accuracy)
2. Go to **Artifacts** tab → click `model/`
3. Click **"Register Model"**
4. Name: `IrisClassifier` → Stage: `Production`

Or do it in code:

```python
# At the end of train_with_mlflow.py, MLflow already registers automatically
# You can also do it manually:
import mlflow
client = mlflow.MlflowClient()
client.transition_model_version_stage(
    name="IrisClassifier",
    version=1,
    stage="Production"
)
```

---

## Step 5 — Load the Model from the Registry

```python
import mlflow.sklearn

# Load directly from the registry — no pickle, no file paths
model = mlflow.sklearn.load_model("models:/IrisClassifier/Production")
predictions = model.predict([[5.1, 3.5, 1.4, 0.2]])
print(predictions)  # ['setosa']
```

---

## Step 6 — Tear Down

```powershell
docker compose down
# Note: ./mlruns folder on your host keeps all experiment data
```

---

## MLflow Tracking Code Pattern

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-experiment")

with mlflow.start_run(run_name="my-run"):
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)

    # ... train your model ...

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("f1", 0.94)

    # Log the model
    mlflow.sklearn.log_model(model, "model")
```

---

## Exercises

1. Run 4+ experiments with different `n_estimators` values. Use the MLflow UI to compare them.
2. Add a confusion matrix image as an artifact: `mlflow.log_artifact("confusion_matrix.png")`
3. Log a metric at each CV fold (not just the mean). Use `mlflow.log_metric("cv_fold_accuracy", score, step=fold_i)`
4. Use the UI's "Models" tab to register a model and transition it through stages: `None → Staging → Production`

---

**Next lesson →** `../03-capstone/`
