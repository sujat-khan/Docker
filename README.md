# 🐳 Docker Mastery — Python MLOps Track

A hands-on Docker course for Python developers learning MLOps.
Every lesson is a real folder. You run real commands. No slides, no videos.

## Prerequisites
- Docker Desktop installed and running ✅
- Python 3.x installed (for a few scripts run locally)
- A terminal (PowerShell on Windows)

---

## 📚 Course Map

```
Docker/
│
├── module-01-fundamentals/         🌱 Beginner
│   ├── 01-hello-world/             Run your first container, understand the flow
│   ├── 02-python-container/        Isolation, bind mounts, env vars
│   └── 03-essential-commands/      Full CLI cheatsheet with hands-on practice
│
├── module-02-dockerfiles/          🌱 Beginner
│   ├── 01-first-dockerfile/        Write and build your first Dockerfile
│   ├── 02-flask-app/               Dockerize a real Flask web API
│   └── 03-dependencies/            Manage requirements.txt + layer caching
│
├── module-03-data-storage/         🔧 Intermediate
│   ├── 01-volumes/                 Persist ML models with Docker volumes
│   └── 02-multi-stage-builds/      Shrink images from 1.2GB → 300MB
│
├── module-04-compose/              🔧 Intermediate
│   ├── 01-networking/              Container networking + service discovery
│   └── 02-ml-stack/                FastAPI + Redis + Postgres via Compose
│
├── module-05-ml-workloads/         🔧 Intermediate
│   ├── 01-sklearn-model/           Train and package a scikit-learn model
│   ├── 02-jupyter/                 Run Jupyter Lab in Docker
│   └── 03-fastapi-serving/         Production ML REST API with FastAPI
│
├── module-06-advanced/             ⚙️ Advanced
│   ├── 01-registries/              Push images to Docker Hub
│   ├── 02-best-practices/          Bad vs Good Dockerfile comparison
│   └── 03-security/                Non-root users, secrets, read-only FS
│
└── module-07-mlops/                🏆 Master
    ├── 01-cicd-github-actions/     Automated build + test + push pipeline
    ├── 02-mlflow/                  Experiment tracking with MLflow in Docker
    └── 03-capstone/                Full MLOps stack: MLflow + MinIO + FastAPI
```

---

## How to Use This Course

1. **Open a lesson folder** in VS Code
2. **Read its `README.md`** — explains the concept and walks you through every step
3. **Look at the files** — `Dockerfile`, `app.py`, `docker-compose.yml`, etc.
4. **Run the commands** in PowerShell exactly as shown in the README
5. **Complete the exercises** at the bottom of each README
6. **Move to the next lesson**

---

## Quick Start

```powershell
# 1. Verify Docker Desktop is running
docker --version
docker info

# 2. Start with lesson 1
cd module-01-fundamentals\01-hello-world
# Then open README.md
```

---

## Learning Path by Goal

| Goal | Start Here |
|------|-----------|
| "I'm totally new to Docker" | `module-01-fundamentals/01-hello-world/` |
| "I want to Dockerize my Python script" | `module-02-dockerfiles/01-first-dockerfile/` |
| "I want to serve an ML model" | `module-05-ml-workloads/03-fastapi-serving/` |
| "I want multi-container apps" | `module-04-compose/02-ml-stack/` |
| "I want CI/CD pipelines" | `module-07-mlops/01-cicd-github-actions/` |
| "I want MLflow tracking" | `module-07-mlops/02-mlflow/` |
| "I want the full MLOps stack" | `module-07-mlops/03-capstone/` |

---

## Key Commands You'll Use

```powershell
docker run <image>                  # Run a container
docker build -t name:tag .          # Build an image from Dockerfile
docker ps -a                        # List all containers
docker images                       # List all images
docker compose up -d                # Start all services in docker-compose.yml
docker compose down                 # Stop and remove all services
docker logs <container>             # View container logs
docker exec -it <container> bash    # Shell into a running container
docker system prune -a              # Clean up all unused resources
```

---

*Total: ~35 lessons across 7 modules | ~12 hours of hands-on practice*
