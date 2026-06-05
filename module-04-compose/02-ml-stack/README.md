# Lesson 1 — Multi-Container ML Stack with Docker Compose

**Module:** Compose | **Level:** 🔧 Intermediate | **Time:** ~25 min

---

## What You'll Learn
- What Docker Compose is and why you need it
- Define multiple services in one `docker-compose.yml`
- Service discovery: containers talk to each other by name
- Use Compose for a real ML stack

---

## The Problem Without Compose

Running an ML stack manually is painful:

```powershell
# You'd have to do all of THIS every time:
docker network create ml-net
docker run -d --name db --network ml-net -e POSTGRES_PASSWORD=secret postgres:15-alpine
docker run -d --name cache --network ml-net redis:7-alpine
docker run -d --name api --network ml-net -p 8000:8000 -e DB_URL=postgresql://... ml-api
# ... and reverse all of it to tear down
```

With Compose:
```powershell
docker compose up -d      # Start everything
docker compose down       # Stop and clean up everything
```

---

## What's in This Stack

```
ml-api (FastAPI)  ──→  redis (caching predictions)
                  ──→  postgres (storing prediction history)
```

All three communicate by service name — no IP addresses needed.

---

## Step 1 — Explore the Files

```
02-ml-stack/
├── docker-compose.yml    ← defines all 3 services
├── api/
│   ├── Dockerfile
│   ├── main.py           ← FastAPI app
│   └── requirements.txt
└── README.md
```

Open `docker-compose.yml` and read it carefully. Every line has a comment.

---

## Step 2 — Start the Stack

```powershell
cd module-04-compose\02-ml-stack

# Build the api image and start all services
docker compose up --build -d
```

---

## Step 3 — Check Everything is Running

```powershell
docker compose ps
# Should show: api (running), redis (running), postgres (running)

docker compose logs
# See startup logs from all services

docker compose logs api
# Only the api service logs
```

---

## Step 4 — Test the API

```powershell
# Health check
Invoke-WebRequest http://localhost:8000/health -UseBasicParsing | Select-Object -Expand Content

# Make a prediction
$body = '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
Invoke-WebRequest http://localhost:8000/predict `
  -Method POST -ContentType "application/json" -Body $body `
  -UseBasicParsing | Select-Object -Expand Content
```

Open **http://localhost:8000/docs** in your browser — FastAPI generates an interactive UI automatically!

---

## Step 5 — Service Discovery in Action

Services communicate using their **service name** as hostname:

```powershell
# Shell into the api container
docker compose exec api bash

# Try connecting to redis by service name (not IP)
python -c "import redis; r = redis.Redis(host='redis', port=6379); print(r.ping())"
# Output: True

# Try reaching postgres by service name
python -c "import psycopg2; print('postgres reachable')"

exit
```

---

## Step 6 — Tear Down

```powershell
# Stop and remove containers (volumes preserved)
docker compose down

# Stop and remove containers AND volumes (database data gone!)
docker compose down -v
```

---

## Key Compose Commands

```powershell
docker compose up -d         # Start in background
docker compose up --build    # Rebuild images then start
docker compose down          # Stop + remove containers
docker compose down -v       # Also remove volumes
docker compose ps            # Status of all services
docker compose logs -f api   # Follow logs for one service
docker compose exec api bash # Shell into a service
docker compose restart api   # Restart one service
docker compose stop api      # Stop one service only
```

---

## Exercises

1. Add a 4th service to the `docker-compose.yml`: `adminer` (image: `adminer`, port 8080) — a PostgreSQL web UI.
2. Stop just the `api` service with `docker compose stop api`. Do postgres and redis stay running?
3. Scale the api: `docker compose up --scale api=2`. What error do you get? Why? (Hint: port conflict)
4. Change something in `api/main.py`, then run `docker compose up --build -d`. Notice only the api service restarts.

---

**Next lesson →** `../../module-05-ml-workloads/01-sklearn-model/`
