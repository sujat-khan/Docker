# Lesson 3 — Docker Security Fundamentals

**Module:** Advanced | **Level:** ⚙️ Advanced | **Time:** ~18 min

---

## What You'll Learn
- Why running as root in Docker is dangerous
- How to handle secrets (passwords, API keys) safely
- Image scanning for vulnerabilities
- The principle of least privilege in containers

---

## Rule 1: Don't Run as Root

By default, containers run as `root`. This is dangerous — if an attacker gets into your container, they have root access.

```dockerfile
# ✅ Create and switch to a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

Verify:
```powershell
# Without USER directive — you're root
docker run --rm python:3.11-slim whoami
# Output: root

# With USER directive — you're appuser
docker run --rm python:3.11-slim bash -c "useradd testuser && su testuser -c whoami"
# Output: testuser
```

---

## Rule 2: Never Put Secrets in the Dockerfile

```dockerfile
# ❌ NEVER DO THIS — the password is baked into the image forever
ENV DATABASE_PASSWORD=super_secret_123
# Anyone who pulls your image can see this!

# ❌ ALSO BAD — visible in docker history
RUN echo "password123" > /app/config.txt
```

### How to Pass Secrets Safely

```powershell
# Option 1: Environment variables at runtime (OK for non-critical secrets)
docker run -e DATABASE_PASSWORD=secret my-app

# Option 2: .env file (better — don't commit to git!)
docker run --env-file .env my-app

# Option 3: Docker secrets (best — for Docker Swarm / Compose)
# Compose example:
# secrets:
#   db_password:
#     file: ./db_password.txt
```

---

## Rule 3: Use Read-Only Filesystem

```powershell
# The container can't write to its own filesystem
docker run --read-only python:3.11-slim python -c "print('hello')"

# If your app needs to write temp files, allow specific dirs
docker run --read-only --tmpfs /tmp python:3.11-slim python -c "
import tempfile, os
with tempfile.NamedTemporaryFile(dir='/tmp', delete=False) as f:
    f.write(b'temp data')
    print(f'Wrote to {f.name}')
"
```

---

## Rule 4: Scan Images for Vulnerabilities

```powershell
# Docker Scout (built into Docker Desktop)
docker scout cves python:3.11-slim

# Or use docker scan (older method)
docker scan python:3.11-slim
```

This shows known vulnerabilities (CVEs) in the base image and installed packages.

---

## Rule 5: Minimize the Attack Surface

Less in the image = fewer things that can be exploited.

```dockerfile
# ❌ Full Python image — has gcc, make, perl, etc.
FROM python:3.11

# ✅ Slim — just Python and essentials
FROM python:3.11-slim

# ✅✅ Even leaner: build in full, run in slim (multi-stage)
FROM python:3.11 AS builder
RUN pip install flask
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
```

---

## Rule 6: Drop Capabilities

Linux capabilities give fine-grained permissions. Drop the ones you don't need:

```powershell
# Drop all capabilities, add back only what's needed
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE my-web-app
```

---

## Rule 7: Don't Use --privileged

```powershell
# ❌ NEVER in production — gives the container almost full host access
docker run --privileged my-app

# This is only needed for very specific cases (Docker-in-Docker, hardware access)
```

---

## Security Checklist

- [ ] Non-root USER in Dockerfile
- [ ] No secrets in Dockerfile or image layers
- [ ] Secrets passed via env vars or Docker secrets at runtime
- [ ] Using slim/alpine base images
- [ ] Images scanned for vulnerabilities regularly
- [ ] Read-only filesystem where possible
- [ ] Capabilities dropped (`--cap-drop ALL`)
- [ ] Never `--privileged` in production
- [ ] `.dockerignore` excludes `.env`, `.git`, secrets

---

## Hands-On: Root vs Non-Root Demo

This lesson includes `demo.py`, `Dockerfile.root`, and `Dockerfile.nonroot`.

### Build and compare:

```powershell
cd module-06-advanced\03-security

# Build the insecure (root) version
docker build -f Dockerfile.root -t security-demo:root .

# Build the secure (non-root) version
docker build -f Dockerfile.nonroot -t security-demo:nonroot .
```

### Run both and compare the output:

```powershell
# Root container — can write to /etc (dangerous!)
docker run --rm security-demo:root

# Non-root container — blocked from writing to /etc (safe)
docker run --rm security-demo:nonroot
```

Notice the difference in `Running as user` and the `/etc write` line.

### Verify manually:

```powershell
# Root container — you are root
docker run --rm security-demo:root whoami
# Output: root

# Non-root container — you are appuser
docker run --rm security-demo:nonroot whoami
# Output: appuser
```

---

## Exercises

1. Build both Dockerfiles and run them. Compare the `/etc write` result.
2. Run `docker scout cves python:3.11-slim` — how many vulnerabilities are reported?
3. Run a container with `--read-only`. Verify you can still write to a `--tmpfs /tmp` directory.
4. Create a `.env` file with `SECRET_KEY=abc123`. Run a container with `--env-file .env` and print the variable inside.
5. Check `docker history security-demo:root` — can you see the layers?

---

**Next lesson →** `../../module-07-mlops/01-cicd-github-actions/`
