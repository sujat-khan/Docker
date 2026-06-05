# Lesson 3 — Managing Dependencies with requirements.txt

**Module:** Dockerfiles | **Level:** 🌱 Beginner | **Time:** ~15 min

---

## What You'll Learn
- Best practices for pinning dependency versions
- How to generate requirements.txt from a virtual environment
- What `--no-cache-dir` does and why you use it
- How to handle system-level (OS) dependencies some Python packages need

---

## Why Pin Versions?

```
# ❌ BAD — could break tomorrow when a new version releases
numpy
pandas
scikit-learn

# ✅ GOOD — exact same versions every time
numpy==1.26.2
pandas==2.1.4
scikit-learn==1.3.2
```

An unpinned dependency might install version `2.0` tomorrow which breaks your code. Docker images should be **reproducible** — same Dockerfile = same result.

---

## How to Generate requirements.txt

### Option 1: From your local virtual environment

```powershell
# Create a virtual env and install what you need
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install numpy pandas scikit-learn

# Freeze exact versions
pip freeze > requirements.txt
```

### Option 2: Write it manually (recommended for Docker)

Keep only what your app actually imports. `pip freeze` includes *everything*, which bloats your image.

```
# requirements.txt — only direct dependencies
flask==3.0.0
scikit-learn==1.3.2
numpy==1.26.2
```

---

## Step 1 — Look at the Files

This lesson has a data processing script that depends on `pandas` and `numpy`.

```
03-dependencies/
├── Dockerfile
├── requirements.txt
├── process_data.py
└── README.md
```

---

## Step 2 — Build and Run

```powershell
cd module-02-dockerfiles\03-dependencies

docker build -t data-processor:v1 .
docker run --rm data-processor:v1
```

---

## Step 3 — Try Adding a Dependency

Edit `requirements.txt` to add `requests==2.31.0`, then rebuild:

```powershell
docker build -t data-processor:v2 .
```

Notice that `numpy` and `pandas` show `CACHED` — only `requests` gets installed fresh.

---

## System Dependencies

Some Python packages need C libraries to compile. For example, `psycopg2` (PostgreSQL driver) needs `libpq-dev`.

```dockerfile
# Install system packages BEFORE pip install
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

**Pattern:** `apt-get update` → `apt-get install` → `rm -rf .../lists/*` (cleanup APT cache to keep image small).

For this course, we avoid this by using pre-built "binary" wheels. For example, `psycopg2-binary` instead of `psycopg2`.

---

## What Does --no-cache-dir Do?

```dockerfile
# Without: pip saves a cache (~50-200MB) in the image — wasted space
RUN pip install -r requirements.txt

# With: no cache stored — smaller image
RUN pip install --no-cache-dir -r requirements.txt
```

Always use `--no-cache-dir` in Docker. You'll never reinstall packages inside the same image.

---

## Exercises

1. Build the image, check its size with `docker images`. Now remove `--no-cache-dir` from the Dockerfile, rebuild, and compare sizes.
2. Add `matplotlib==3.8.2` to requirements.txt. Rebuild. Does numpy get reinstalled? Why or why not?
3. Try pinning to a version that doesn't exist: `numpy==99.99.99`. What error do you get during build?
4. Look at the Dockerfile — what happens if you swap the order of `COPY requirements.txt .` and `COPY . .`?

---

**Next lesson →** `../../module-03-data-storage/01-volumes/`
