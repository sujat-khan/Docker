# Lesson 1 — Dockerizing a Scikit-Learn Model

**Module:** ML Workloads | **Level:** 🔧 Intermediate | **Time:** ~20 min

---

## What You'll Learn
- Package a trained ML model inside a Docker image
- The "bake model into image" vs "load from volume" tradeoff
- Test predictions from a containerized model

---

## Two Approaches to Packaging Models

### Approach 1: Bake Into Image
```dockerfile
COPY models/iris_model.pkl /app/models/
```
- ✅ Self-contained — image has everything it needs
- ✅ Versioned — `my-model:v3` always has model v3
- ❌ Large images if model is big (GPT-like models = tens of GB)

### Approach 2: Load from Volume at Runtime
```powershell
docker run -v ml-models:/app/models my-model-server
```
- ✅ Small images — model files are external
- ✅ Swap models without rebuilding
- ❌ Need to manage volumes separately

**This lesson uses Approach 1. The Volumes lesson (Module 3) covered Approach 2.**

---

## Step 1 — Train the Model

```powershell
cd module-05-ml-workloads\01-sklearn-model

# Train locally and save the .pkl file
docker build -t sklearn-model .
docker run --rm sklearn-model python train.py
```

Wait — that trains inside Docker but the file stays in the container. Let's save it:

```powershell
# Train and save to a local folder using bind mount
docker run --rm -v "${PWD}/models:/app/models" sklearn-model python train.py

# Verify the model file exists locally
ls models/
```

---

## Step 2 — Build the Prediction Image

Now rebuild — the Dockerfile copies `models/` into the image:

```powershell
docker build -t sklearn-model:v1 .
```

---

## Step 3 — Run Predictions

```powershell
# Interactive prediction
docker run --rm sklearn-model:v1 python predict.py

# Pass features via environment variables
docker run --rm -e "FEATURES=5.1,3.5,1.4,0.2" sklearn-model:v1 python predict.py
```

---

## Step 4 — Iterate on the Model

```powershell
# Train with different hyperparameters
docker run --rm -v "${PWD}/models:/app/models" \
  -e N_ESTIMATORS=200 \
  -e MAX_DEPTH=10 \
  sklearn-model python train.py

# Rebuild image with the new model
docker build -t sklearn-model:v2 .

# Compare predictions from v1 and v2
docker run --rm sklearn-model:v1 python predict.py
docker run --rm sklearn-model:v2 python predict.py
```

---

## Exercises

1. Train the model, build the image, and run predictions. Change `N_ESTIMATORS` and compare.
2. Run `docker images sklearn-model` — how big is the image?
3. Add a new script `evaluate.py` that loads the model and prints accuracy on the test set. Build and run it.
4. What happens if you build the image *before* running `train.py`? (No model file exists yet.)

---

**Next lesson →** `../02-jupyter/`
