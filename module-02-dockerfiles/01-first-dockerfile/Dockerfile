# ── BASE IMAGE ─────────────────────────────────────────
# We start FROM an official Python image.
# "slim" = stripped down, no extras. Smaller = faster to pull/build.
# Always pin a specific version in production (not just "python:latest")
FROM python:3.11-slim

# ── METADATA ───────────────────────────────────────────
# Labels are informational only — like name tags on the image
LABEL maintainer="sujatkhan24@gmail.com"
LABEL version="1.0"
LABEL description="My first custom Docker image"
LABEL course="docker-mastery"

# ── ENVIRONMENT VARIABLES ──────────────────────────────
# PYTHONUNBUFFERED=1   → print() shows up in docker logs immediately (no buffering)
# PYTHONDONTWRITEBYTECODE=1 → don't create .pyc files (keeps image cleaner)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ── WORKING DIRECTORY ──────────────────────────────────
# All subsequent commands (COPY, RUN, CMD) use /app as their working directory
# Docker creates /app if it doesn't exist
WORKDIR /app

# ── COPY FILES ─────────────────────────────────────────
# COPY <source on host>  <destination in image>
# The "." means everything in the build context (current folder on host)
# The "." destination means /app (our WORKDIR)
COPY . .

# ── DEFAULT COMMAND ────────────────────────────────────
# What runs when you do "docker run my-first-image"
# Use JSON array format (exec form) — safer than shell form
CMD ["python", "app.py"]
