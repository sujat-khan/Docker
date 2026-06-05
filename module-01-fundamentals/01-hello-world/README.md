# Lesson 1 — Hello World Container

**Module:** Fundamentals | **Level:** 🌱 Beginner | **Time:** ~10 min

---

## What You'll Learn
- How `docker run` works step by step
- What happens when Docker finds/doesn't find an image locally
- How to inspect containers after they run

---

## Concept: The docker run Flow

When you type `docker run hello-world`, Docker does this:

```
docker run hello-world
        │
        ▼
1. Check local image cache  →  Not found
        │
        ▼
2. Pull from Docker Hub     →  library/hello-world:latest
        │
        ▼
3. Create a container       →  from the image
        │
        ▼
4. Run it                   →  prints message, then exits
```

---

## Step 1 — Verify Docker is Running

Open PowerShell and run:

```powershell
docker --version
# Expected: Docker version 24.x.x or similar

docker info
# Shows Docker engine details, running containers count, etc.
```

If `docker info` gives an error → open Docker Desktop first and wait for it to start.

---

## Step 2 — Run Your First Container

```powershell
docker run hello-world
```

**Read the output carefully.** Docker itself explains what it just did. You'll see:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## Step 3 — Run a Python Container

```powershell
# Pull and run an interactive Python 3.11 shell INSIDE a container
docker run -it python:3.11-slim python
```

You're now inside Python running **inside Docker**. Try:

```python
>>> import sys
>>> print(sys.version)      # Should show 3.11.x
>>> print("Hello Docker!")
>>> exit()
```

**Flags used:**
| Flag | Meaning |
|------|---------|
| `-i` | Interactive — keep stdin open |
| `-t` | Allocate a terminal (TTY) |
| `-it` | Combined: gives you an interactive shell |

---

## Step 4 — Inspect What's Left Behind

```powershell
# List all containers, including stopped ones
docker ps -a

# You should see your hello-world and python containers listed
# STATUS will show "Exited (0)" — they ran and finished cleanly

# List all downloaded images
docker images
# You'll see: hello-world, python (3.11-slim)
```

---

## Step 5 — Run Python One-Liner (no interactive shell)

```powershell
# Run a Python command directly, container exits when done
docker run --rm python:3.11-slim python -c "print('Hello from Docker!')"

# --rm means: automatically delete the container after it exits
# Keeps things clean
```

---

## Step 6 — Cleanup

```powershell
# Remove all stopped containers
docker container prune

# When prompted, type: y
```

---

## Exercises

1. Run `docker run hello-world` a second time. Notice it's faster — why? (Hint: look at the first line of output)
2. Run `docker run -it python:3.9-slim python` (note: Python **3.9** not 3.11). Verify the version inside.
3. Open Docker Desktop — can you find the images and containers in the GUI?
4. Run `docker run --rm python:3.11-slim python -c "import platform; print(platform.platform())"` — what OS does Docker report?

---

## Key Takeaways

- `docker run <image>` = pull (if needed) + create + start a container
- Containers are **disposable** — they stop when their process exits
- `--rm` is your friend during learning: keeps things tidy
- The same Python image works the same on Windows, Mac, Linux

---

**Next lesson →** `../02-python-container/`
