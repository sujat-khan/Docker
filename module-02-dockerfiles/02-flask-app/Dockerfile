FROM python:3.11-slim

# Prevent Python from buffering stdout (critical for docker logs to work)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_ENV=production

WORKDIR /app

# ── LAYER CACHING TRICK ────────────────────────────────
# Copy requirements FIRST — before any other code.
# This layer only rebuilds if requirements.txt changes.
# Your code changes won't force a pip reinstall.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── COPY APPLICATION CODE ──────────────────────────────
# This happens AFTER pip install, so code changes are cheap.
COPY . .

# Document the port (informational — doesn't actually open it)
EXPOSE 5000

# ── START COMMAND ──────────────────────────────────────
# Use gunicorn (production WSGI server) instead of Flask's dev server.
# --workers 2  = handle 2 requests simultaneously
# app:app      = the "app" variable in the "app" module
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
