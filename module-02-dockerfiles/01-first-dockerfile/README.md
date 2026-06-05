# Lesson 1 — Writing Your First Dockerfile

**Module:** Dockerfiles | **Level:** 🌱 Beginner | **Time:** ~20 min

---

## What You'll Learn
- What a Dockerfile is and how to write one
- How Docker layers work (and why they matter for speed)
- Build your first custom image from scratch

---

## Concept: Dockerfile = Recipe for an Image

```
Dockerfile Instructions  →  Image Layers  →  Image  →  Container
─────────────────────────────────────────────────────────────────
FROM python:3.11-slim    →  Layer 1 (base OS + Python)
WORKDIR /app             →  Layer 2 (create directory)
COPY requirements.txt .  →  Layer 3 (your file)
RUN pip install ...      →  Layer 4 (installed packages)
COPY . .                 →  Layer 5 (rest of code)
CMD ["python", "app.py"] →  (metadata — not a layer)
```

**Key insight:** Each layer is cached. If nothing changed in a layer, Docker reuses the cache and skips rebuilding it. This makes subsequent builds fast.

---

## Dockerfile Instruction Reference

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Base image to build from | `FROM python:3.11-slim` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host to image | `COPY . .` |
| `RUN` | Execute a shell command during build | `RUN pip install flask` |
| `ENV` | Set environment variable | `ENV PYTHONUNBUFFERED=1` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 5000` |
| `CMD` | Default command when container starts | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Fixed executable (CMD becomes args) | `ENTRYPOINT ["python"]` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |
| `LABEL` | Add metadata to image | `LABEL maintainer="you@email.com"` |

---

## Step 1 — Look at the Files in This Folder

```
01-first-dockerfile/
├── Dockerfile        ← the recipe
├── app.py            ← the Python script
├── .dockerignore     ← files to exclude from the build
└── README.md
```

Open `Dockerfile` and read every line and its comment.

---

## Step 2 — Build the Image

```powershell
# Make sure you're in this folder
cd module-02-dockerfiles\01-first-dockerfile

# Build the image
# -t = tag (name:version)
# .  = build context (current directory)
docker build -t my-first-image:v1 .
```

Watch the output — you'll see each layer being built:
```
[+] Building 15.3s (6/6) FINISHED
 => [1/4] FROM python:3.11-slim          ← pull base image
 => [2/4] WORKDIR /app                   ← set directory
 => [3/4] COPY . .                       ← copy your files
 => [4/4] ...                            ← (no RUN here)
 => exporting to image
```

---

## Step 3 — Run It

```powershell
# Run with default settings
docker run --rm my-first-image:v1

# Pass your name via environment variable
docker run --rm -e YOUR_NAME="Alice" my-first-image:v1

# See the image you built
docker images
```

---

## Step 4 — Rebuild and See Caching

Change something in `app.py` (e.g., the print message), then rebuild:

```powershell
# Edit app.py first, then:
docker build -t my-first-image:v2 .
```

Notice `CACHED` next to layers that didn't change — Docker reuses them. **This is why layer order matters.**

---

## Step 5 — Inspect the Image

```powershell
# See all layers and their sizes
docker history my-first-image:v1

# See detailed metadata (JSON)
docker inspect my-first-image:v1
```

---

## .dockerignore — Like .gitignore

The `.dockerignore` file tells Docker which files NOT to copy into the build context. This:
- Speeds up builds (less data sent to Docker engine)
- Keeps images smaller and cleaner
- Prevents secrets from leaking into images

---

## Exercises

1. Build the image, run it, then change `app.py` and rebuild. Compare the build times.
2. Add a `LABEL` to the Dockerfile (e.g., `LABEL course="docker-mastery"`). Rebuild and check `docker inspect` to see your label.
3. Change the CMD to print a different message without changing the WORKDIR. Rebuild and run.
4. Try to run the image without building first: `docker run --rm my-first-image:nonexistent`. What error do you get?

---

**Next lesson →** `../02-flask-app/`
