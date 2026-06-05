# Lesson 1 — Docker Networking Basics

**Module:** Compose | **Level:** 🔧 Intermediate | **Time:** ~15 min

---

## What You'll Learn
- How containers communicate with each other
- Docker network types: bridge, host, none
- Create custom networks and connect containers by name
- Port mapping: how traffic flows from your browser to a container

---

## Concept: Container Isolation

By default, each container is isolated. Two containers **cannot** talk to each other unless they're on the same Docker network.

```
Container A ──╳──▶ Container B     (different networks = blocked)
Container A ──✓──▶ Container B     (same network = works)
```

---

## Network Types

| Type | Description | Use Case |
|------|-------------|----------|
| `bridge` | Default. Private internal network. Containers get internal IPs. | Most use cases |
| `host` | Container shares the host's network directly. No port mapping needed. | Performance (Linux only) |
| `none` | No networking. Fully isolated. | Security-sensitive containers |

---

## Step 1 — See the Default Network

```powershell
# List all Docker networks
docker network ls

# You'll see:
# bridge   — the default network
# host     — host mode
# none     — no network
```

---

## Step 2 — Containers Can't Talk by Default

```powershell
# Start two containers on the default bridge network
docker run -d --name server1 python:3.11-slim python -c "import time; time.sleep(300)"
docker run -d --name server2 python:3.11-slim python -c "import time; time.sleep(300)"

# Try to ping server1 FROM server2 by name — FAILS on default bridge
docker exec server2 python -c "import socket; socket.gethostbyname('server1')"
# Error: socket.gaierror: Name or service not known

# Clean up
docker rm -f server1 server2
```

**Why?** The default `bridge` network doesn't support DNS resolution by container name. You need a **custom network**.

---

## Step 3 — Create a Custom Network

```powershell
# Create a custom bridge network
docker network create ml-network

# Start containers ON that network
docker run -d --name server1 --network ml-network python:3.11-slim python -c "import time; time.sleep(300)"
docker run -d --name server2 --network ml-network python:3.11-slim python -c "import time; time.sleep(300)"

# Now they CAN find each other by name!
docker exec server2 python -c "import socket; print(socket.gethostbyname('server1'))"
# Output: 172.18.0.2 (or similar internal IP)
```

---

## Step 4 — Run a Real Example

Let's connect a Python HTTP server to a client:

```powershell
# Start a Python HTTP server container
docker run -d --name web --network ml-network python:3.11-slim python -m http.server 8080

# From another container, make a request to it BY NAME
docker exec server2 python -c "
import urllib.request
response = urllib.request.urlopen('http://web:8080')
print(f'Status: {response.status}')
print('Containers are talking to each other!')
"
```

---

## Step 5 — Port Mapping Explained

Port mapping lets traffic from your host machine reach inside a container.

```
Your Browser → http://localhost:8080
                    │
                    │  -p 8080:80  (host_port:container_port)
                    ▼
              Container (nginx listening on port 80)
```

```powershell
# Map host port 9090 → container port 8080
docker run -d --name web-public -p 9090:8080 --network ml-network python:3.11-slim python -m http.server 8080

# Access from your browser: http://localhost:9090
# Access from other containers: http://web-public:8080 (internal port)
```

---

## Step 6 — Clean Up

```powershell
docker rm -f server1 server2 web web-public
docker network rm ml-network
```

---

## Network Commands Reference

```powershell
docker network create my-net           # Create a custom network
docker network ls                      # List networks
docker network inspect my-net          # See which containers are connected
docker network connect my-net <ctr>    # Connect a running container
docker network disconnect my-net <ctr> # Disconnect a container
docker network rm my-net               # Delete a network
docker network prune                   # Delete all unused networks
```

---

## Key Takeaways

- Default bridge network: containers get IPs but **no DNS** (can't use names)
- Custom networks: containers can reach each other **by name** (service discovery)
- Docker Compose automatically creates a custom network for all services (that's why it "just works")
- `-p host:container` maps ports so your browser can reach containers

---

## Exercises

1. Create a network called `test-net`. Start two containers on it. Verify they can resolve each other by name.
2. Start a container without `--network`. Can it resolve containers on `test-net`?
3. Use `docker network inspect test-net` to find the IP addresses of connected containers.
4. Start a container with `-p 7777:8080`. Verify you can access it at `http://localhost:7777`.

---

**Next lesson →** `../02-ml-stack/`
