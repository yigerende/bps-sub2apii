# bps-sub2api 部署

本项目基于 `ranxi2001/sub2api` 的 `production` 分支，保留原有请求转发、账号调度、计费和 BPS 功能。
本次同步的上游提交为 `3dafea660a0a9c1a607c914a0391ddf916673811`（2026-09-28）。
代码仓库：<https://github.com/yigerende/bps-sub2apii>。项目和 Docker 镜像名称为 `bps-sub2api`，仓库地址末尾有两个 `i`。

## 与已有 sub2api 并行部署

| 资源 | 本项目默认值 |
| --- | --- |
| Compose 项目 | `bps-sub2api` |
| 应用容器和服务 | `bps-sub2api` |
| PostgreSQL 容器和服务 | `bps-sub2api-postgres` |
| Redis 容器和服务 | `bps-sub2api-redis` |
| 应用镜像 | `ghcr.io/yigerende/bps-sub2api:latest` |
| 宿主机端口 | `8082`，容器内部仍为 `8080` |
| 默认数据库及数据库用户 | `bps-sub2api` |
| 默认网络 | `bps-sub2api_bps-sub2api-network` |
| 命名卷 | `bps-sub2api_bps-sub2api-data`、`bps-sub2api_bps-sub2api-postgres-data`、`bps-sub2api_bps-sub2api-redis-data` |

PostgreSQL 和 Redis 仅通过本项目的内部网络访问，不映射宿主机端口。全套部署使用新的数据库和 Redis 实例。
请使用独立部署目录和新生成的 `.env`；不要复制旧项目的配置、数据目录或 `COMPOSE_PROJECT_NAME`，也不要用 `docker compose -p sub2api` 启动本项目。
如果 `8082` 已被其他服务占用，只修改本项目 `.env` 中的 `SERVER_PORT`。

## Linux 推荐部署方式

仓库每次推送 `production` 分支会通过 `Build bps-sub2api image` 工作流构建 amd64 和 arm64 镜像。
首次部署前，先在仓库 Actions 中确认该工作流成功；GHCR 私有包需要先 `docker login ghcr.io`，或由仓库所有者将对应包设置为公开。

```bash
mkdir -p /opt/bps-sub2api
cd /opt/bps-sub2api
curl -fsSL https://raw.githubusercontent.com/yigerende/bps-sub2apii/production/deploy/docker-deploy.sh -o docker-deploy.sh
bash docker-deploy.sh
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps
docker compose logs -f bps-sub2api
```

初始化脚本生成数据库密码、JWT 密钥和 TOTP 加密密钥，保存在当前目录 `.env`。
页面访问地址为 `http://服务器IP:8082`。管理员初始密码可在 `.env` 配置，未配置时按原项目逻辑从首次启动日志查看。
反向代理应连接新的 `8082` 端口，使用独立域名；原站点继续连接其原端口。

该脚本使用独立绑定目录：`./bps-sub2api-data`、`./bps-sub2api-postgres-data`、`./bps-sub2api-redis-data`。

## 从源码构建

```bash
git clone --branch production https://github.com/yigerende/bps-sub2apii.git bps-sub2api
cd bps-sub2api
docker build -t ghcr.io/yigerende/bps-sub2api:latest .
cd deploy
cp .env.example .env
chmod 600 .env
# 编辑 .env，至少设置独立且安全的 POSTGRES_PASSWORD。
docker compose up -d --pull never
```

仓库内默认 `deploy/docker-compose.yml` 使用独立命名卷；`docker-compose.local.yml` 使用独立绑定目录。
`docker-compose.dev.yml` 从源码构建，使用 `bps-sub2api-dev` 项目和带 `-dev` 的容器名。
`docker-compose.standalone.yml` 面向外部数据库和 Redis，需要显式指定地址；并行部署优先使用包含独立数据库和 Redis 的完整配置。

## 更新与备份

始终进入本项目独立目录执行：

```bash
cd /opt/bps-sub2api
docker compose pull
docker compose up -d
```

维护命令中的服务名分别是 `bps-sub2api`、`bps-sub2api-postgres`、`bps-sub2api-redis`。
停止服务使用 `docker compose down`；需要保留数据时不要加 `-v`。
绑定目录部署可以在停止本项目后备份整个 `/opt/bps-sub2api`，其中包含 `.env` 和三个数据目录。

安装脚本、systemd 服务、二进制和 Release 包均使用 `bps-sub2api` 名称。
后台版本更新仅查询 `yigerende/bps-sub2apii` 的 Release，避免更新成来源仓库的二进制。首次正式 Release 发布前可直接通过 Docker 镜像更新。
