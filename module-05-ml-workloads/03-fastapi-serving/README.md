# Lesson 3 — FastAPI ML Model Serving

**Module:** ML Workloads | **Level:** 🔧 Intermediate | **Time:** ~25 min

---

## What You'll Learn
- Build a production-quality REST API for ML model predictions
- Use FastAPI + Pydantic for automatic validation and docs
- Package model + API into a single deployable Docker image
- Test with FastAPI's auto-generated Swagger UI

---

## Why FastAPI for ML Serving?

| Feature | Flask | FastAPI |
|---------|-------|---------|
| Speed | Moderate | **3-10x faster** (async ASGI) |
| Type validation | Manual | **Automatic** (Pydantic) |
| API docs | Must install Swagger separately | **Built-in** at `/docs` |
| Async support | Add-on | **Native** |
| Modern Python | Works | **Uses type hints natively** |

---

## Project Structure

```
03-fastapi-serving/
├── app/
│   ├── __init__.py
│   └── main.py          ← FastAPI application
├── train.py              ← Train and save model
├── models/               ← Created by train.py
│   └── iris_model.pkl
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Step 1 — Train and Save the Model

```powershell
cd module-05-ml-workloads\03-fastapi-serving

# Build the image
docker build -t iris-api .

# Train the model (saves to local ./models/)
docker run --rm -v "${PWD}/models:/app/models" iris-api python train.py
```

---

## Step 2 — Rebuild with the Model Baked In

```powershell
# Now rebuild — COPY will include models/iris_model.pkl
docker build -t iris-api:v1 .
```

---

## Step 3 — Start the API

```powershell
docker run -d -p 8000:8000 --name iris-api iris-api:v1
```

---

## Step 4 — Test It!

### In your browser
Open **http://localhost:8000/docs** — this is FastAPI's auto-generated interactive API documentation. You can test every endpoint directly from the browser.

### From the terminal

```powershell
# Health check
Invoke-WebRequest http://localhost:8000/health -UseBasicParsing | Select-Object -Expand Content

# Make a prediction
$body = '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
Invoke-WebRequest http://localhost:8000/predict `
  -Method POST -ContentType "application/json" -Body $body `
  -UseBasicParsing | Select-Object -Expand Content

# Expected response:
# {
#   "prediction": "setosa",
#   "confidence": 0.98,
#   "probabilities": {"setosa": 0.98, "versicolor": 0.01, "virginica": 0.01}
# }

# Model info
Invoke-WebRequest http://localhost:8000/model-info -UseBasicParsing | Select-Object -Expand Content
```

---

## Step 5 — View Logs

```powershell
docker logs iris-api
# You'll see uvicorn startup and request logs
```

---

## Step 6 — Cleanup

```powershell
docker stop iris-api && docker rm iris-api
```

---

## Key Patterns

### Pydantic Request Validation
FastAPI uses Pydantic models to automatically validate inputs:
```python
class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., ge=0)  # ge=0 means "must be >= 0"
```
If someone sends `sepal_length: -5`, FastAPI returns a `422 Validation Error` automatically.

### Model Loading at Startup
```python
@asynccontextmanager
async def lifespan(app):
    # Load model once when server starts, not on every request
    global model
    model = pickle.load(open("models/iris_model.pkl", "rb"))
    yield
```

### Auto-Generated Docs
FastAPI generates:
- **Swagger UI** at `/docs` — interactive testing
- **ReDoc** at `/redoc` — clean API documentation
Both are free, automatic, and always up-to-date.

---

## Exercises

1. Start the API and test all endpoints using the Swagger UI at `/docs`.
2. Send a request with a negative sepal_length. What error do you get? (Pydantic validation!)
3. Add a new `POST /batch-predict` endpoint that accepts a list of features and returns a list of predictions.
4. Add a `GET /model-info` endpoint that returns the model type, feature names, and accuracy.
5. Run the container with `--restart unless-stopped`. Kill the process inside and watch it auto-restart.

---

**Next lesson →** `../../module-06-advanced/01-registries/`
