# Lesson 1 — Docker Registries & Pushing Images

**Module:** Advanced | **Level:** ⚙️ Advanced | **Time:** ~15 min

---

## What You'll Learn
- What a Docker registry is (Docker Hub, ECR, GCR)
- How to push your images to Docker Hub
- Tagging strategies for versioning images

---

## Concept: Image Registry

A registry is like GitHub, but for Docker images:

```
Your Machine                Docker Hub
┌───────────────┐           ┌───────────────────┐
│ my-ml-api:v1  │──push──▶  │ username/my-ml-api│
│ my-ml-api:v2  │           │  :v1              │
└───────────────┘           │  :v2              │
                            │  :latest          │
     Server B               │                   │
┌───────────────┐           │                   │
│               │◀──pull──  │                   │
│ my-ml-api:v2  │           └───────────────────┘
└───────────────┘
```

---

## Step 1 — Create a Docker Hub Account

1. Go to **https://hub.docker.com** and sign up (free)
2. Remember your username — you'll need it for tagging

---

## Step 2 — Log In from the Terminal

```powershell
docker login
# Enter your Docker Hub username and password
# Or use an access token (recommended — Settings → Security → Access Tokens)
```

---

## Step 3 — Tag Your Image

Images must be tagged as `username/image-name:tag` to push:

```powershell
# Assuming you built iris-api:v1 in a previous lesson
# Tag it for Docker Hub
docker tag iris-api:v1 YOUR_USERNAME/iris-api:v1
docker tag iris-api:v1 YOUR_USERNAME/iris-api:latest
```

---

## Step 4 — Push

```powershell
docker push YOUR_USERNAME/iris-api:v1
docker push YOUR_USERNAME/iris-api:latest
```

Your image is now public. Anyone can pull it with:
```powershell
docker pull YOUR_USERNAME/iris-api:v1
```

---

## Step 5 — Pull on Another Machine

To prove it works, remove the local image and pull from the registry:

```powershell
docker rmi YOUR_USERNAME/iris-api:v1
docker run YOUR_USERNAME/iris-api:v1
# Docker pulls from Hub → runs it
```

---

## Tagging Best Practices

```powershell
# Version tags (most important)
my-app:v1.0.0
my-app:v1.0.1

# Git commit SHA tags (for traceability)
my-app:git-a1b2c3d

# Environment tags
my-app:staging
my-app:production

# Always tag latest too
my-app:latest
```

| Strategy | When to Use |
|----------|-------------|
| Semantic versioning (`v1.2.3`) | Releases |
| Git SHA (`git-abc123`) | CI/CD pipelines |
| `latest` | Always — points to newest |
| `dev` / `staging` / `prod` | Environment-specific builds |

---

## Popular Registries

| Registry | Provider | Free Tier |
|----------|----------|-----------|
| Docker Hub | Docker | 1 private repo, unlimited public |
| GitHub Container Registry | GitHub | Free with GitHub account |
| AWS ECR | Amazon | Pay per storage |
| Google Artifact Registry | Google Cloud | Pay per storage |
| Azure ACR | Microsoft | Pay per storage |

---

## Exercises

1. Create a Docker Hub account (if you don't have one), login, tag an image, and push it.
2. Delete the local image and pull it back from Docker Hub. Verify it runs.
3. Tag the same image with 3 different tags (`:v1`, `:latest`, `:dev`). Push all 3. How much storage does it use? (Hint: layers are shared)
4. Try pushing without logging in first. What error do you get?

---

**Next lesson →** `../02-best-practices/`
