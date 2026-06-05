# Lesson 2 — Dockerizing a Python Flask App

**Module:** Dockerfiles | **Level:** 🌱 Beginner | **Time:** ~20 min

---

## What You'll Learn
- How to install Python packages with pip inside Docker
- Why you copy `requirements.txt` BEFORE your code (layer caching)
- How to expose and map ports
- Access a web app running inside a container from your browser

---

## Concept: Layer Caching Optimization

This is one of the most important Docker tricks:

```
❌ NAIVE ORDER (slow on every code change):
   COPY . .
   RUN pip install -r requirements.txt
   ↑ Every code change = re-install ALL packages

✅ OPTIMIZED ORDER (fast after first build):
   COPY requirements.txt .        ← only changes when deps change
   RUN pip install ...            ← cached unless requirements.txt changes
   COPY . .                       ← code changes only rebuild this layer
```

The rule: **put things that change least frequently near the top of your Dockerfile.**

---

## Project Files

```
02-flask-app/
├── Dockerfile
├── requirements.txt
├── app.py          ← Flask application
└── .dockerignore
```

---

## Step 1 — Look at the Code

Open `app.py` — it's a simple Flask app with 3 routes:
- `GET /` → returns info about the running container
- `GET /health` → health check endpoint (important for production!)
- `POST /echo` → echoes back JSON you send

Open `requirements.txt` — only two dependencies: Flask and Gunicorn.

---

## Step 2 — Build the Image

```powershell
cd module-02-dockerfiles\02-flask-app

docker build -t flask-demo:v1 .
```

Watch pip install Flask — this takes a moment on the first build.

---

## Step 3 — Run the Flask App

```powershell
# -d  = run in background (detached)
# -p 5000:5000 = map host port 5000 to container port 5000
# --name = easy-to-remember name
docker run -d -p 5000:5000 --name flask-demo flask-demo:v1
```

---

## Step 4 — Test It

Open your browser: **http://localhost:5000**

Or use PowerShell:

```powershell
# Test the root endpoint
Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing | Select-Object -Expand Content

# Test health check
Invoke-WebRequest -Uri http://localhost:5000/health -UseBasicParsing | Select-Object -Expand Content

# POST request (echo endpoint)
$body = '{"model": "random_forest", "version": "v2.1"}'
Invoke-WebRequest -Uri http://localhost:5000/echo `
  -Method POST `
  -ContentType "application/json" `
  -Body $body `
  -UseBasicParsing | Select-Object -Expand Content

# Or with curl if you have it:
curl http://localhost:5000/health
```

---

## Step 5 — View Logs

```powershell
# See what's being logged (gunicorn startup + request logs)
docker logs flask-demo

# Follow logs in real time — make some requests and watch
docker logs -f flask-demo
# Ctrl+C to stop following
```

---

## Step 6 — Test Layer Caching

Make a small change to `app.py` (e.g., add a word to a message). Then:

```powershell
docker build -t flask-demo:v2 .
```

Notice: `pip install` shows `CACHED` — it wasn't re-run because `requirements.txt` didn't change. Only the `COPY . .` step re-ran.

Now change `requirements.txt` (e.g., add a version number) and rebuild:

```powershell
docker build -t flask-demo:v3 .
```

Notice: pip install runs again because `requirements.txt` changed.

---

## Step 7 — Stop & Clean Up

```powershell
docker stop flask-demo
docker rm flask-demo
```

---

## Why host="0.0.0.0"?

```python
# ❌ WRONG for Docker — only accepts connections from within the container
app.run(host="127.0.0.1", port=5000)

# ✅ CORRECT — accepts connections from outside the container
app.run(host="0.0.0.0", port=5000)
```

`0.0.0.0` means "listen on all network interfaces". Without it, port mapping (`-p 5000:5000`) doesn't work — your browser can't reach the app.

---

## Exercises

1. Run the container without `-d` (remove the flag). What's different? (Press Ctrl+C to stop)
2. Change the port mapping: `-p 8080:5000`. Which URL do you use in your browser now?
3. Add a new route to `app.py`: `GET /python-version` that returns the Python version. Rebuild and test.
4. Run `docker inspect flask-demo` while it's running and find the container's IP address and port binding.

---

**Next lesson →** `../03-dependencies/`
