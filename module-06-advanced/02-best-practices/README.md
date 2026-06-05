# Lesson 2 — Dockerfile Best Practices & Optimization

**Module:** Advanced | **Level:** ⚙️ Advanced | **Time:** ~20 min

---

## What You'll Learn
- Write production-quality Dockerfiles
- Common mistakes and how to avoid them
- Minimize image size and build time

---

## The Rules

### 1. Use Specific Base Image Tags

```dockerfile
# ❌ BAD — "latest" could change anytime
FROM python:latest

# ✅ GOOD — pinned version, predictable
FROM python:3.11.7-slim-bullseye
```

### 2. Use slim/alpine Images

```
python:3.11        → ~1 GB
python:3.11-slim   → ~130 MB    ← use this
python:3.11-alpine → ~50 MB     ← smallest, but may have issues with some C libs
```

### 3. Copy Requirements Before Code

```dockerfile
# ✅ Layer caching — pip only re-runs when requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### 4. Combine RUN Commands

```dockerfile
# ❌ BAD — each RUN creates a layer
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get clean

# ✅ GOOD — one layer, and clean up in the same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*
```

### 5. Don't Run as Root

```dockerfile
# Create a non-root user
RUN useradd --create-home appuser
USER appuser
```

### 6. Use .dockerignore

```
__pycache__/
.git/
.env
*.log
.venv/
node_modules/
```

### 7. Set PYTHONUNBUFFERED=1

```dockerfile
ENV PYTHONUNBUFFERED=1    # print() shows up in docker logs immediately
ENV PYTHONDONTWRITEBYTECODE=1  # no .pyc files
```

### 8. Use HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
```

---

## Compare: Before & After

Look at the two Dockerfiles in this folder:

```powershell
cd module-06-advanced\02-best-practices

# Build the "bad" version
docker build -f Dockerfile.bad -t demo:bad .

# Build the "good" version
docker build -f Dockerfile.good -t demo:good .

# Compare sizes
docker images demo
```

---

## Step 1 — Examine Both Dockerfiles

Open `Dockerfile.bad` and `Dockerfile.good`. Each line in the bad version has a comment explaining what's wrong.

---

## Step 2 — Build and Compare

```powershell
docker build -f Dockerfile.bad -t demo:bad .
docker build -f Dockerfile.good -t demo:good .

# Compare image sizes
docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" | findstr demo

# Compare layer count
docker history demo:bad --no-trunc
docker history demo:good --no-trunc
```

---

## Step 3 — Test Both

```powershell
docker run --rm demo:bad
docker run --rm demo:good
# Same output — but very different image quality
```

---

## Checklist for Production Dockerfiles

- [ ] Pinned base image version (e.g., `python:3.11.7-slim-bullseye`)
- [ ] Using slim or alpine variant
- [ ] `.dockerignore` exists and covers `.git/`, `__pycache__/`, `.env`
- [ ] `COPY requirements.txt` before `COPY . .`
- [ ] `--no-cache-dir` on pip install
- [ ] `PYTHONUNBUFFERED=1` set
- [ ] RUN commands combined with `&&`
- [ ] APT cache cleaned in same layer
- [ ] Non-root user if possible
- [ ] HEALTHCHECK defined for web services
- [ ] LABEL with maintainer and version

---

## Exercises

1. Build both Dockerfiles and compare sizes. How much smaller is the "good" version?
2. Add a `HEALTHCHECK` to one of your previous Flask/FastAPI Dockerfiles.
3. Modify a Dockerfile to run as a non-root user. Verify by running `whoami` inside the container.
4. Look at `docker history` for both images — identify the biggest layers.

---

**Next lesson →** `../03-security/`
