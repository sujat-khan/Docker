# Lesson 1 — CI/CD with Docker & GitHub Actions

**Module:** MLOps | **Level:** 🏆 Master | **Time:** ~30 min

---

## What You'll Learn
- What CI/CD means and why Docker makes it powerful
- Write a GitHub Actions workflow that builds and pushes Docker images
- Automated testing before deployment
- Image tagging strategy for production

---

## Concept: CI/CD Pipeline

```
Developer pushes code to GitHub
        │
        ▼
GitHub Actions automatically:
   1. Checks out code
   2. Runs Python tests (pytest)
   3. Builds Docker image
   4. Pushes to Docker Hub
   5. (Optional) Deploys to server
        │
        ▼
🚀 New version running in production
```

**CI (Continuous Integration):** Test every code change automatically.
**CD (Continuous Delivery):** Deploy tested code automatically.

---

## Step 1 — Understand the Workflow

Look at the workflow file in this folder: `.github/workflows/docker-publish.yml`

It defines:
- **Trigger:** Runs on push to `main` branch
- **Job 1 (test):** Install deps, run pytest
- **Job 2 (build-and-push):** Build Docker image, push to Docker Hub (only if tests pass)

---

## Step 2 — Set Up (What You'd Do in a Real Repo)

### Create Docker Hub Access Token
1. Go to https://hub.docker.com → Account Settings → Security
2. Click "New Access Token" → Give it a name → Copy the token

### Add GitHub Secrets
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add two secrets:
   - `DOCKER_USERNAME` = your Docker Hub username
   - `DOCKER_TOKEN` = the access token you just created

---

## Step 3 — Read the Workflow File

Open `.github/workflows/docker-publish.yml` in this folder. Every section is commented.

Key parts:
```yaml
on:
  push:
    branches: [main]    # Trigger on push to main

jobs:
  test:                  # First: run tests
    steps:
      - run: pytest tests/ -v

  build-and-push:        # Then: build & push
    needs: test          # Only if tests pass!
    steps:
      - uses: docker/build-push-action@v5
```

---

## Step 4 — The Test File

Look at `tests/test_api.py` — it tests the Flask API endpoints:

```python
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
```

---

## Step 5 — Try It Locally First

Before CI/CD, always verify locally:

```powershell
cd module-07-mlops\01-cicd-github-actions

# Build
docker build -t cicd-demo .

# Run tests inside Docker
docker run --rm cicd-demo pytest tests/ -v

# Run the app
docker run --rm -p 5000:5000 cicd-demo
```

---

## How It Works in Practice

```
1. You push code to GitHub
2. GitHub sees .github/workflows/docker-publish.yml
3. It spins up a fresh Ubuntu VM
4. Runs your tests
5. If tests pass → builds Docker image → pushes to Docker Hub
6. You get a ✅ or ❌ badge on the commit

Every pushed image is tagged with:
  - latest         (always the newest)
  - git-abc1234    (the git commit SHA)
```

---

## Exercises

1. Read the workflow YAML file carefully. Identify: what triggers it, what jobs run, what order.
2. Build and run the app locally. Run `pytest tests/ -v` inside Docker.
3. If you have a GitHub repo, copy the `.github/` folder there, add the Docker Hub secrets, and push. Watch the Actions tab!
4. Add a new test for a new endpoint. Push and verify the CI catches a failing test (intentionally break something).

---

**Next lesson →** `../02-mlflow/`
