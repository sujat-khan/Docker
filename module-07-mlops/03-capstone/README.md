# Capstone — Full MLOps Pipeline

**Module:** MLOps | **Level:** 🏆 Master | **Time:** ~60 min

---

## What You're Building

A complete, production-inspired MLOps system:

```
┌─────────────────────────────────────────────────────────┐
│                  docker compose up                       │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │ Training │───▶│  MLflow  │───▶│  Prediction API  │  │
│  │ Script   │    │ Tracking │    │    (FastAPI)      │  │
│  └──────────┘    │    UI    │    └──────────────────┘  │
│                  └────┬─────┘             │             │
│  ┌──────────┐         │          ┌────────┴──────┐      │
│  │  MinIO   │◀────────┘          │  PostgreSQL   │      │
│  │(artifact │                    │  (metadata)   │      │
│  │ storage) │                    └───────────────┘      │
│  └──────────┘                                           │
└─────────────────────────────────────────────────────────┘

Ports:
  http://localhost:5000  → MLflow Tracking UI
  http://localhost:8000  → Prediction API + /docs
  http://localhost:9001  → MinIO Console (artifact storage)
```

---

## Prerequisites

Complete all previous modules first. You should be comfortable with:
- Writing Dockerfiles ✅
- Docker Compose ✅
- FastAPI ML serving ✅

---

## Step 1 — Start the Infrastructure

```powershell
cd module-07-mlops\03-capstone

docker compose up -d
```

Wait ~20 seconds for all services to start.

```powershell
docker compose ps
# All should show "running"
```

---

## Step 2 — Initialize MinIO Bucket

MinIO needs a bucket created before MLflow can use it:

```powershell
docker compose run --rm minio-init
```

---

## Step 3 — Run a Training Experiment

```powershell
docker compose run --rm trainer python train.py
```

You'll see:
```
Experiment: iris-classification
Run: rf-n100-depth5
  accuracy   : 0.9667
  f1_weighted: 0.9664
  cv_accuracy: 0.9667
Model registered as: IrisClassifier
```

---

## Step 4 — View Results in MLflow UI

Open **http://localhost:5000** in your browser.

You'll see:
- The experiment `iris-classification`
- The run with all logged parameters and metrics
- The model artifact stored in MinIO

---

## Step 5 — Run More Experiments (Compare Models)

```powershell
# Run with different hyperparameters
docker compose run --rm trainer python train.py --n-estimators 200 --max-depth 10

# Run a logistic regression comparison
docker compose run --rm trainer python train.py --model logistic
```

Go back to the MLflow UI → compare runs side by side.

---

## Step 6 — Promote a Model to Production

In the MLflow UI:
1. Click on a run → "Artifacts" → "Register Model"
2. Name it `IrisClassifier`, stage: `Production`

Or do it via Python:

```powershell
docker compose run --rm trainer python promote_model.py
```

---

## Step 7 — Test the Prediction API

```powershell
# Health check
Invoke-WebRequest http://localhost:8000/health -UseBasicParsing | Select-Object -Expand Content

# Predict
$body = '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
Invoke-WebRequest http://localhost:8000/predict `
  -Method POST -ContentType "application/json" -Body $body `
  -UseBasicParsing | Select-Object -Expand Content
```

Or open **http://localhost:8000/docs** for the interactive API.

---

## Step 8 — Tear Down

```powershell
docker compose down -v   # Remove everything including volumes
```

---

## Final Exercises (Master Level)

1. Add a `GET /experiments` endpoint to the API that lists MLflow experiments
2. Write a Python script that automatically promotes the best model (by accuracy) to Production
3. Modify the `docker-compose.yml` to add a **Grafana** service for monitoring
4. Add a GitHub Actions workflow (in `.github/workflows/`) that runs `train.py` automatically when data changes

---

## 🎓 Congratulations!

You've completed the Docker Mastery course. You now know how to:

- ✅ Build Docker images for Python applications
- ✅ Write optimized Dockerfiles with layer caching
- ✅ Persist data with volumes
- ✅ Orchestrate multi-container stacks with Compose
- ✅ Serve ML models with FastAPI
- ✅ Track experiments with MLflow in Docker
- ✅ Understand the architecture of a real MLOps pipeline

**Next steps:** Kubernetes (`kubectl`), Helm charts, AWS ECS/EKS, Terraform
