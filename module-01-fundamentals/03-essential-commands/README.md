# Lesson 3 — Essential Docker Commands Cheatsheet

**Module:** Fundamentals | **Level:** 🌱 Beginner | **Time:** ~15 min

This lesson is a **hands-on cheatsheet**. Run every command, read the output, and understand what it does.

---

## Container Lifecycle

### Create & Run

```powershell
# Most basic: run a container, stream output, exit when done
docker run python:3.11-slim python -c "print('hello')"

# Give the container a name (easier to reference later)
docker run --name my-python python:3.11-slim python -c "print('named container')"

# Run in background (detached) — you get your terminal back
docker run -d --name bg-container python:3.11-slim python -c "import time; time.sleep(60)"

# Run, then auto-delete when finished (best for one-off tasks)
docker run --rm python:3.11-slim python -c "print('gone after this')"
```

### Inspect

```powershell
# List RUNNING containers only
docker ps

# List ALL containers (running + stopped + created)
docker ps -a

# View logs from a container
docker logs my-python

# Follow logs in real time (Ctrl+C to stop)
docker logs -f bg-container

# See detailed JSON info about a container
docker inspect my-python

# Show resource usage (CPU, RAM) of running containers
docker stats
```

### Control

```powershell
# Stop a running container (graceful — sends SIGTERM, waits 10s, then SIGKILL)
docker stop bg-container

# Start a stopped container again
docker start my-python

# Restart
docker restart my-python

# Remove a stopped container
docker rm my-python

# Force remove a running container (skip graceful stop)
docker rm -f bg-container
```

### Execute Commands Inside

```powershell
# Open an interactive bash shell in a RUNNING container
docker exec -it bg-container bash

# Run a single command in a running container
docker exec bg-container python -c "import sys; print(sys.version)"
```

---

## Image Management

```powershell
# List downloaded images
docker images

# Pull an image without running it
docker pull python:3.9-slim

# Pull a specific version tag
docker pull python:3.11.7-slim-bullseye

# Remove an image
docker rmi python:3.9-slim

# Show image history (all the layers)
docker history python:3.11-slim

# Search Docker Hub from the command line
docker search python
```

---

## Cleanup (Important!)

Docker uses disk space. Clean up regularly:

```powershell
# Remove ALL stopped containers
docker container prune

# Remove ALL unused images (not referenced by any container)
docker image prune

# Remove ALL unused images (including tagged ones)
docker image prune -a

# Remove unused volumes
docker volume prune

# Nuclear: remove all unused containers, images, networks, volumes
docker system prune -a

# Show how much disk Docker is using
docker system df
```

---

## Hands-On Practice

Run these in order and check each output:

```powershell
# 1. Start a background container that sleeps for 5 minutes
docker run -d --name practice python:3.11-slim python -c "import time; print('starting...'); time.sleep(300)"

# 2. Check it's running
docker ps

# 3. View its log
docker logs practice

# 4. Execute a command inside it
docker exec practice python -c "print('I am alive!')"

# 5. Stop it
docker stop practice

# 6. Check it's stopped (it will be in docker ps -a)
docker ps -a

# 7. Start it again
docker start practice

# 8. Remove it forcefully (while it's running)
docker rm -f practice

# 9. Confirm it's gone
docker ps -a
```

---

## Most Common Flags Reference

| Flag | Short for | Effect |
|------|-----------|--------|
| `-d` | `--detach` | Run in background |
| `-it` | `--interactive --tty` | Interactive terminal |
| `--rm` | — | Auto-remove on exit |
| `--name` | — | Give container a name |
| `-p 8080:80` | `--publish` | Map host port 8080 → container port 80 |
| `-v ./src:/app` | `--volume` | Bind mount a directory |
| `-e KEY=VAL` | `--env` | Set environment variable |
| `-w /app` | `--workdir` | Set working directory |

---

## Exercises

1. Run `docker stats` while a container is running — what do you see? (`Ctrl+C` to exit)
2. Pull `alpine:latest` (a tiny Linux image, ~5MB). Run `docker run --rm alpine echo "tiny!"`. Then check its size with `docker images`.
3. Run `docker inspect` on any container and find the container's IP address in the output.
4. After running a few containers, run `docker system df` — how much space is being used?

---

**Next lesson →** `../../module-02-dockerfiles/01-first-dockerfile/`
