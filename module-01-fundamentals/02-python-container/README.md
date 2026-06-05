# Lesson 2 — Running Python Scripts in Containers

**Module:** Fundamentals | **Level:** 🌱 Beginner | **Time:** ~15 min

---

## What You'll Learn
- How to run a Python script from your machine inside a container
- What bind mounts are (briefly — deep dive in Module 3)
- The difference between the container's filesystem and your own

---

## The Problem: Containers Are Isolated

A container has its OWN filesystem. Your files on `C:\` don't exist inside it.

```
Your Machine:              Container:
C:\Users\sujat\           /
  projects\               /app/         ← empty by default
    Docker\
      my_script.py        ← NOT visible inside container!
```

To get your files in, you have two options:
1. **Copy them in** (using `COPY` in a Dockerfile — next module)
2. **Mount them** (using `-v` — bind mount)

---

## Step 1 — Look at the Script

Open `hello.py` in this folder:

```python
# hello.py is already here — look at it!
```

Run it locally first:
```powershell
python hello.py
```

---

## Step 2 — Run It Inside Docker Using a Bind Mount

```powershell
# Make sure you're in this lesson's folder
cd module-01-fundamentals\02-python-container

# Mount the current directory into /app inside the container
# Then run hello.py from /app
docker run --rm -v "${PWD}:/app" -w /app python:3.11-slim python hello.py
```

**Flags breakdown:**
| Flag | What it does |
|------|-------------|
| `--rm` | Remove container after exit |
| `-v "${PWD}:/app"` | Mount current folder (`${PWD}`) to `/app` inside container |
| `-w /app` | Set working directory inside container to `/app` |
| `python hello.py` | The command to run inside the container |

---

## Step 3 — Prove the Isolation

```powershell
# Shell into a container WITHOUT mounting anything
docker run --rm -it python:3.11-slim bash

# Inside the container, try:
ls /app          # No such directory!
ls /             # Only Docker's default filesystem
cat /etc/os-release  # See what Linux distro this is
exit
```

Now mount and check:

```powershell
docker run --rm -it -v "${PWD}:/app" -w /app python:3.11-slim bash

# Inside the container now:
ls /app          # Your files are here!
cat hello.py     # You can read your script
python hello.py  # Run it
exit
```

---

## Step 4 — Run the Data Analysis Script

```powershell
# Run the more complex data script
docker run --rm -v "${PWD}:/app" -w /app python:3.11-slim python data_info.py
```

Notice: `data_info.py` uses only the Python standard library — no pip install needed.
If it used numpy, you'd get an ImportError (we fix that in Module 2 with Dockerfiles).

---

## Step 5 — Pass Environment Variables

```powershell
# Pass variables into the container with -e
docker run --rm -v "${PWD}:/app" -w /app \
  -e STUDENT_NAME="Alice" \
  -e COURSE="Docker MLOps" \
  python:3.11-slim python greet.py
```

---

## Exercises

1. Edit `hello.py` (change the message), then re-run the docker command. The change appears instantly — why? (The file is mounted, not copied)
2. Run `docker run --rm python:3.11-slim python -c "import os; print(os.listdir('/app'))"` without `-v`. What error do you get?
3. Try: `docker run --rm -v "${PWD}:/app" -w /app python:3.11-slim python -c "import os; print(os.listdir('.'))"`. List your mounted files.

---

## Key Takeaways

- Containers have isolated filesystems — your local files aren't automatically there
- `-v host_path:container_path` mounts a directory from your machine into the container
- `-w /app` sets the working directory so Python finds your scripts
- This is great for development — changes on your machine instantly appear in the container

---

**Next lesson →** `../03-essential-commands/`
