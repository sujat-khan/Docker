# Lesson 1 — Docker Volumes: Persisting ML Data

**Module:** Data & Storage | **Level:** 🔧 Intermediate | **Time:** ~20 min

---

## Why This Matters for ML

By default, when you **delete a container**, everything inside it disappears:
- 8-hour training run → model weights → **gone**
- 50GB preprocessed dataset → **gone**
- Experiment logs → **gone**

Volumes solve this. Data in a volume **survives** container deletion.

---

## Two Ways to Persist Data

### Named Volumes (Docker-managed)
```powershell
# Docker stores the data in its own area (usually in C:\ProgramData\docker\volumes\)
docker run -v my-volume:/app/models my-image
```
**Best for:** Production data, model artifacts, databases

### Bind Mounts (Host folder)
```powershell
# You choose the folder on your machine
docker run -v C:\my-project\models:/app/models my-image
# or on PowerShell:
docker run -v "${PWD}/models:/app/models" my-image
```
**Best for:** Development (live code editing, sharing files easily)

---

## Hands-On: Train a Model and Save It

### Step 1 — Build the training image

```powershell
cd module-03-data-storage\01-volumes

docker build -t sklearn-trainer .
```

### Step 2 — Create a named volume for models

```powershell
docker volume create ml-models

# Inspect it (find where Docker stores it on Windows)
docker volume inspect ml-models
```

### Step 3 — Train and save (model persists in volume)

```powershell
docker run --rm -v ml-models:/app/models sklearn-trainer python train.py
```

You'll see output like:
```
Training RandomForestClassifier...
Test accuracy: 0.9667
Model saved to /app/models/iris_model.pkl
```

The container exits and is removed (`--rm`). But the **model is still in the volume**.

### Step 4 — Load the model in a NEW container

```powershell
# New container, same volume — model is still there!
docker run --rm -v ml-models:/app/models sklearn-trainer python load_and_predict.py
```

### Step 5 — Prove it survives container deletion

```powershell
# Remove all containers related to this (they're already gone with --rm)
# Check the volume still exists and has data
docker volume ls
docker volume inspect ml-models

# Mount the volume and browse files inside
docker run --rm -v ml-models:/app/models python:3.11-slim ls /app/models
```

---

## Bind Mount: Live Development

```powershell
# Mount your local ./models folder into the container
# Changes on your machine appear instantly in the container
docker run --rm -v "${PWD}/models:/app/models" sklearn-trainer python train.py

# Now check your local ./models folder — the .pkl file is there!
ls models/
```

---

## Volume Commands Reference

```powershell
docker volume create ml-models          # Create a named volume
docker volume ls                        # List all volumes
docker volume inspect ml-models         # Detailed info (including mount path)
docker volume rm ml-models              # Delete a volume
docker volume prune                     # Delete ALL unused volumes
```

---

## Exercises

1. Run `train.py`, delete the container, then use `load_and_predict.py` in a new container. Confirm the model loads.
2. Create a second volume `ml-experiments`. Mount both volumes and save metadata to one, model to the other.
3. Use a bind mount to save the model to your local `./models/` folder. Open it in Python locally (outside Docker).
4. What happens if you `docker volume rm ml-models` while a container is using it? Try it!

---

**Next lesson →** `../02-multi-stage-builds/`
