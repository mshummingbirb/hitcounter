# hitcounter

A small web-based hit counter built to demonstrate Python (Flask), Redis, Docker, and Kubernetes. Each visit to the web page atomically increments a Redis-backed counter and displays the current count and the serving container/pod hostname.

## Components
- `app` (HTTP service): main Flask app (`app.py`) with two routes:
  - `/` — increments Redis key `hits` and displays the count plus hostname.
  - `/healthz` — returns 200 OK for liveness/readiness probes.
- Redis (data store): stores the hit counter in the `hits` key. The app uses environment variables `REDIS_HOST` and `REDIS_PORT`.
- `Dockerfile`: builds the container image (Python 3.11-slim), installs dependencies from `requirements.txt`, and runs the app on port 5000.
- `docker-compose.yml`: local development compose file that runs `redis` and the web app together.
- `requirements.txt`: Python dependencies (`Flask>=2.0`, `redis>=4.0`).
- `k8s/manifest.yaml`: Kubernetes manifests that create the `hitcounter` Namespace, Redis Deployment+Service, and hitcounter Deployment+Service (LoadBalancer) with readiness/liveness probes.

## How it works (brief)
- The Flask app connects to Redis using `REDIS_HOST` and `REDIS_PORT`.
- Each GET to `/` calls `redis_client.incr("hits")` to increment the counter atomically.
- The app includes the container/pod hostname retrieved with `socket.gethostname()` in the response.
- If Redis cannot be reached, the page shows a fallback message.
- `/healthz` is used by Kubernetes probes to check application health.

## Run locally (no Docker)
1. Ensure Redis is running locally (or set `REDIS_HOST` to a reachable Redis).
2. Create a virtualenv, install dependencies, run the app:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open: http://localhost:5000

## Run locally with Docker Compose
Build and start Redis + web:
```bash
docker-compose up --build
```
Open: http://localhost:5000

## Build and run the container manually
Build the image:
```bash
docker build -t my-hit-counter:v1 .
```
Run Redis and the app (example):
```bash
docker run -d --name redis -p 6379:6379 redis:7
docker run -p 5000:5000 --env REDIS_HOST=host.docker.internal my-hit-counter:v1
```
If both containers run on the same Docker network, set `REDIS_HOST` to the redis container name.

## Deploy to Kubernetes
The `k8s/manifest.yaml` includes:
- Namespace: `hitcounter`
- Redis Deployment + Service (`redis-service`)
- Hitcounter Deployment (replicas: 2) with `REDIS_HOST=redis-service`, liveness/readiness probes on `/healthz`
- Service `hitcounter-service` (type: LoadBalancer) mapping port 80 → container port 5000

Apply the manifest:
```bash
kubectl apply -f k8s/manifest.yaml
```
Notes:
- The manifest's hitcounter image is `mshummingbirb/my-hit-counter:v3`. Replace this with your built/pushed image tag.
- If your cluster lacks LoadBalancer support, use `NodePort` or an Ingress instead.

## Troubleshooting
- "Could not connect to Redis database": verify `REDIS_HOST`/`REDIS_PORT` and network connectivity from the app container/pod.
- Image pull errors: confirm image name/tag and registry access; use `imagePullSecrets` for private registries.
- Debugging: `kubectl logs <pod>` and `kubectl describe pod <pod>` give logs and events.

## Next steps / ideas
- Track counts per-host or per-path (use Redis hashes).
- Add Prometheus metrics and Grafana dashboards.
- Add graceful shutdown handling and structured request logging.
- Add CI to build/push images and update Kubernetes manifests.
- Add Terraform to provision cloud infra and a managed Redis.
