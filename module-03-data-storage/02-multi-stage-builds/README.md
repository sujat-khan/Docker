# Lesson 2 — Multi-Stage Builds for Lean Images

**Module:** Data & Storage | **Level:** 🔧 Intermediate | **Time:** ~20 min

---

## What You'll Learn
- Why Docker images get bloated and how to fix it
- Multi-stage builds: use one image to build, another to run
- Reduce a Python ML image from ~1.2GB to ~300MB

---

## The Problem: Image Bloat

When you install packages, build tools come along:
- `gcc`, `g++` — C compilers (needed to build numpy, scipy, etc.)
- Header files, development libraries
- `pip` cache

These are needed during `pip install` but **not** when your app runs. Multi-stage builds let you throw them away.

---

## Concept: Multi-Stage Build

```dockerfile
# STAGE 1: "builder" — install everything (heavy)
FROM python:3.11 AS builder
RUN pip install numpy scikit-learn flask

# STAGE 2: "runtime" — copy only what's needed (light)
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["python", "app.py"]
```

The final image only has Stage 2. Stage 1 is discarded.

---

## Step 1 — Build the Regular Image (Bloated)

```powershell
cd module-03-data-storage\02-multi-stage-builds

# Build the "naive" version (single-stage)
docker build -f Dockerfile.naive -t ml-app:naive .

# Check size
docker images ml-app:naive
# Probably ~1.0-1.4 GB
```

---

## Step 2 — Build the Multi-Stage Image (Lean)

```powershell
docker build -f Dockerfile.multistage -t ml-app:lean .

# Check size
docker images ml-app:lean
# Should be ~300-500 MB — much smaller!
```

---

## Step 3 — Verify Both Work Identically

```powershell
docker run --rm ml-app:naive
docker run --rm ml-app:lean
# Same output from both!
```

---

## Step 4 — Compare Sizes

```powershell
docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" | findstr ml-app
```

You'll see something like:
```
ml-app:naive    1.23GB
ml-app:lean     389MB
```

---

## When to Use Multi-Stage Builds

| Scenario | Use Multi-Stage? |
|----------|-----------------|
| Production deployment | ✅ Yes — smaller = faster pull, less attack surface |
| Learning / Development | ❌ Usually not — adds complexity, slower iteration |
| CI/CD pipelines | ✅ Yes — smaller images push/pull faster |
| ML training images | ⚠️ Maybe — if GPU tools are big, worth trimming |

---

## Exercises

1. Compare the sizes of `ml-app:naive` and `ml-app:lean`. How much space did you save?
2. Add `matplotlib` to the requirements. Rebuild both. How does it affect the size difference?
3. Run `docker history ml-app:naive` and `docker history ml-app:lean` — compare the layers.
4. Try a 3-stage build: builder → testing → runtime (add a stage that runs pytest before the final copy).

---

**Next lesson →** `../../module-04-compose/01-networking/`
