# Lesson 2 — Running Jupyter Notebooks in Docker

**Module:** ML Workloads | **Level:** 🔧 Intermediate | **Time:** ~15 min

---

## What You'll Learn
- Run Jupyter Lab inside Docker with a single command
- Persist notebooks using volumes (don't lose your work!)
- Use the official Jupyter Docker images

---

## Why Jupyter in Docker?

- **Reproducibility:** Everyone on the team gets the exact same Jupyter environment
- **Clean machine:** No need to install Jupyter, numpy, pandas locally
- **Disposable:** Break something? Delete container, start fresh
- **Share easily:** "Run this Dockerfile" beats a 20-step setup guide

---

## Option 1: The Official Jupyter Image (Fastest)

No Dockerfile needed — just run:

```powershell
# Basic Jupyter Lab with Python
docker run --rm -p 8888:8888 \
  -v "${PWD}/notebooks:/home/jovyan/work" \
  jupyter/scipy-notebook

# Or with more ML libraries (pandas, sklearn, matplotlib, seaborn)
docker run --rm -p 8888:8888 \
  -v "${PWD}/notebooks:/home/jovyan/work" \
  jupyter/scipy-notebook
```

Open the URL printed in the terminal (includes a token): `http://127.0.0.1:8888/lab?token=...`

---

## Option 2: Custom Jupyter Image (This Lesson)

When you need specific packages, build your own:

```powershell
cd module-05-ml-workloads\02-jupyter

docker build -t ml-jupyter .
docker run --rm -p 8888:8888 -v "${PWD}/notebooks:/app/notebooks" ml-jupyter
```

Open **http://localhost:8888** in your browser (no token needed — we disabled it for local dev).

---

## Step 1 — Build and Start

```powershell
cd module-05-ml-workloads\02-jupyter

# Build the custom image
docker build -t ml-jupyter .

# Run with notebooks folder mounted
docker run --rm -p 8888:8888 -v "${PWD}/notebooks:/app/notebooks" ml-jupyter
```

---

## Step 2 — Create a Notebook

1. Open **http://localhost:8888** in your browser
2. Navigate to the `notebooks/` folder (it's your mounted volume)
3. Create a new Python 3 notebook
4. Run some code:

```python
import numpy as np
import pandas as pd
import sklearn
print(f"numpy: {np.__version__}")
print(f"pandas: {pd.__version__}")
print(f"sklearn: {sklearn.__version__}")
```

5. Save the notebook

---

## Step 3 — Verify Persistence

```powershell
# Stop the container (Ctrl+C)
# Check your local notebooks/ folder — the .ipynb file is there!
ls notebooks/

# Restart the container — your notebook is still there
docker run --rm -p 8888:8888 -v "${PWD}/notebooks:/app/notebooks" ml-jupyter
```

The bind mount (`-v`) means your notebooks live on **your machine**, not inside the container. Deleting the container doesn't delete your work.

---

## Step 4 — Run in Background

```powershell
# -d = detached (background)
docker run -d --name jupyter -p 8888:8888 -v "${PWD}/notebooks:/app/notebooks" ml-jupyter

# Check logs for any output
docker logs jupyter

# Stop when done
docker stop jupyter && docker rm jupyter
```

---

## Exercises

1. Start the Jupyter container and create a notebook that trains a model. Save it. Stop the container. Restart and verify the notebook is still there.
2. Install a new package from inside Jupyter: `!pip install seaborn`. Now restart the container. Is seaborn still installed? Why not? How would you fix this?
3. Try the official image: `docker run --rm -p 8888:8888 jupyter/scipy-notebook`. Compare what packages are available.
4. Create a notebook that reads a CSV file from the mounted `notebooks/` folder.

---

**Next lesson →** `../03-fastapi-serving/`
