# bps-sub2api Docker deployment

Image: `ghcr.io/yigerende/bps-sub2api:latest` (Linux amd64 and arm64).
Repository: <https://github.com/yigerende/bps-sub2apii>.

Use the maintained Compose files and follow [the deployment guide](../docs/BPS_DEPLOY.md).
They isolate the Compose project, application, PostgreSQL, Redis, networks and persistent storage from an existing sub2api deployment.
The default host port is `8082`; the application still listens on port `8080` inside its container.

```bash
mkdir -p /opt/bps-sub2api
cd /opt/bps-sub2api
curl -fsSL https://raw.githubusercontent.com/yigerende/bps-sub2apii/production/deploy/docker-deploy.sh -o docker-deploy.sh
bash docker-deploy.sh
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose logs -f bps-sub2api
```

PostgreSQL and Redis stay on the private Compose network without published host ports.
Use a separate directory and the newly generated `.env`; do not reuse the existing installation's data or Compose project name.

The production branch image workflow publishes `latest` and immutable `sha-<commit>` tags.
The Release workflow publishes versioned tags when a release is created.
Wait for the relevant image workflow to succeed before pulling a newly published image.
