# ReAgent · 部署方案

## 📋 目录

- [部署架构](#部署架构)
- [环境说明](#环境说明)
- [快速开始（开发环境）](#快速开始开发环境)
- [生产部署](#生产部署)
- [基础设施清单](#基础设施清单)
- [依赖服务](#依赖服务)
- [Nginx 配置说明](#nginx-配置说明)
- [CI/CD 流程](#cicd-流程)
- [运维指南](#运维指南)
- [故障排查](#故障排查)

---

## 🏗 部署架构

```
                          ┌─────────────┐
                          │   Cloudflare │
                          │   (DNS/CDN)  │
                          └──────┬──────┘
                                 │
                            ┌────▼────┐
                            │  Nginx  │
                            │ (Proxy) │
                            └────┬────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
              ┌─────▼─────┐ ┌───▼────┐ ┌─────▼─────┐
              │  ReAgent   │ │        │ │            │
              │   API x2   │ │        │ │  Redirect  │
              │  (FastAPI) │ │  Redis │ │  Static    │
              └─────┬─────┘ │ (Cache)│ │  Assets    │
                    │       └────────┘ └────────────┘
              ┌─────▼─────┐
              │ PostgreSQL │  (Optional — production)
              │  or SQLite │
              └───────────┘
```

### 流量路径

```
用户 → Cloudflare (HTTPS) → Nginx (反向代理) → ReAgent API
                                ↓
                         OpenAPI/Anthropic → 外部 AI API
```

### 服务拓扑（单机部署）

```
┌─────────────────────────────────────────┐
│               Server Host                │
│  ┌─────────┐  ┌────────┐  ┌─────────┐   │
│  │ ReAgent │  │ Redis  │  │  Nginx  │   │
│  │ :8000   │  │ :6379  │  │ :80/443 │   │
│  └─────────┘  └────────┘  └─────────┘   │
│  ┌──────────────────────────────────┐    │
│  │  Docker Volume: outputs/        │    │
│  │  Docker Volume: data/           │   │
│  │  Docker Volume: redis_data/     │   │
│  └──────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## 🌱 环境说明

| 环境 | 用途 | 配置 | 资源 |
|------|------|------|------|
| **dev** | 本地开发 | 热重载、SQLite、Mock LLM | 本地机器 |
| **test** | CI/预发布 | SQLite/内存、Mock LLM | 轻量 VPS |
| **prod** | 生产 | PostgreSQL、Redis、SSL | 生产 VPS |

### 环境配置对照

| 配置项 | dev | test | prod |
|--------|-----|------|------|
| Debug | ✅ true | ✅ true | ❌ false |
| Log Level | DEBUG | INFO | INFO |
| 数据库 | SQLite | SQLite | SQLite/PostgreSQL |
| Redis | ✅ | ✅ | ✅ |
| 热重载 | ✅ | ❌ | ❌ |
| Nginx | ❌ | ❌ | ✅ |
| SSL | ❌ | ❌ | ✅ |
| AI 模型 | gpt-4o | gpt-4o-mini | gpt-4o |
| API Workers | 1 | 2 | 4+ |

---

## 🚀 快速开始（开发环境）

### 前置条件

- Docker & Docker Compose v2
- 已配置 `.env` 文件（API Key 等）

### 启动

```bash
# 1. 进入项目根目录
cd /path/to/reagent

# 2. 配置环境变量
cp deploy/.env.dev .env
# 编辑 .env，填入你的 API Key

# 3. 启动开发环境
make dev
# 或直接：
docker compose -f deploy/docker-compose.yml --profile dev up

# 4. 验证
curl http://localhost:8000/api/v1/health
```

### 开发调试

```bash
# 查看日志
make dev-logs
docker compose -f deploy/docker-compose.yml --profile dev logs -f

# 停止
make dev-down

# 重新构建
make dev-build

# 运行测试
make test

# 代码格式化
make format

# 代码检查
make lint
```

---

## 📦 生产部署

### 1. 服务器准备

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y docker.io docker-compose-v2 curl ufw

# 启动 Docker
sudo systemctl enable --now docker

# 防火墙
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. 克隆与配置

```bash
git clone <repo-url> /opt/reagent
cd /opt/reagent

# 生产环境配置
cp deploy/.env.prod .env
vi .env   # 填入所有敏感值
```

### 3. 启动

```bash
# 构建并启动所有服务
docker compose -f deploy/docker-compose.yml --profile prod up -d

# 验证运行状态
docker compose -f deploy/docker-compose.yml --profile prod ps

# 健康检查
curl -k https://localhost/api/v1/health
```

### 4. HTTPS 配置（Let's Encrypt）

```bash
# 安装 certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 更新 nginx.conf 中的证书路径
```

### 5. 扩容

```bash
# 增加 API 实例（在 docker-compose.yml 中调整 replicas）
docker compose -f deploy/docker-compose.yml --profile prod up -d --scale api=3
```

---

## 📊 基础设施清单

### 最低配置（Phase 1 MVP）

| 资源 | 规格 | 月预估成本 |
|------|------|-----------|
| **VPS (单机)** | 2 vCPU / 4GB RAM / 50GB SSD | $15-25 |
| **域名** | 1 个 | $10-15/年 |
| **Cloudflare** | Free 套餐 | $0 |
| **OpenAI API** | Pay-as-you-go | $200-500 |
| **Anthropic API** | Pay-as-you-go | $100-300 |
| **Redis** | 内嵌 (Docker) | $0 |
| **合计** | | **$325-840/月** |

### 推荐配置（Phase 1 生产）

| 资源 | 规格 | 月预估成本 |
|------|------|-----------|
| **VPS (主)** | 4 vCPU / 8GB RAM / 100GB SSD | $40-80 |
| **VPS (备)** | 2 vCPU / 4GB RAM / 50GB SSD | $20-40 |
| **域名 x2** | 主域 + 备用 | $20-30/年 |
| **Managed Redis** | 1GB (Upstash/Redis Cloud) | $15-30 |
| **对象存储** | S3-compatible (Backblaze B2 / R2) | $5-15 |
| **监控 (可选)** | UptimeRobot / Grafana Cloud Free | $0 |
| **OpenAI API** | 预估月消耗 | $2,000-5,000 |
| **Anthropic API** | 预估月消耗 | $500-2,000 |
| **合计** | | **$2,580-7,165/月** |

> 💡 成本大头在 AI API 调用。可根据用量选择模型降配：
> - 文案类 → gpt-4o-mini / claude-haiku（大幅降低成本）
> - 分析类 → gpt-4o / claude-sonnet（需要高质量）

---

## 🧩 依赖服务

| 服务 | 用途 | 必选 | 生产替代方案 |
|------|------|------|------------|
| **Redis** | 缓存、会话、限速 | ✅ | Upstash / Redis Cloud |
| **SQLite** | 轻量存储 | ✅ (dev) | — |
| PostgreSQL | 生产级存储 | ❌ (可选) | RDS / Supabase / 自建 |
| **FFmpeg** | 视频处理 | ✅ | 系统安装 |
| **Pillow** | 图片生成 | ✅ | 已包含在 Python 依赖 |
| **Jinja2** | 模板渲染 | ✅ | 已包含 |
| S3 兼容 | 素材存储 | ❌ (可选) | Backblaze B2 / Cloudflare R2 |
| **Nginx** | 反向代理 | ✅ (prod) | Caddy / Traefik |

### Redis 用途详解

```
┌── Redis ──────────────────────────────────────────┐
│ ┌─────────────────────┐  ┌──────────────────────┐ │
│ │ Rate Limiter (IP)   │  │ Session Store (JWT)  │ │
│ ├─────────────────────┤  ├──────────────────────┤ │
│ │ AI Response Cache   │  │ Throttle Locks       │ │
│ └─────────────────────┘  └──────────────────────┘ │
└────────────────────────────────────────────────────┘
```

---

## 🔒 Nginx 配置说明

生产环境使用 `nginx.conf` 实现：
- **SSL 终结** — 处理 HTTPS 流量，后端保持 HTTP
- **反向代理** — 负载均衡到多个 API 实例
- **静态资源服务** — 直接提供 `/outputs/` 素材
- **SSE 流式支持** — 关闭 proxy_buffering 确保实时推送
- **Gzip 压缩** — JSON API 响应压缩
- **安全头** — X-Frame-Options 等

---

## 🚦 CI/CD 流程

### CI Pipeline (`.github/workflows/ci.yml`)

```
┌──────────┐   ┌────────┐   ┌──────────┐
│  Lint    │ → │  Test  │ → │  Docker  │
│ (Ruff)   │   │(pytest)│   │  Build   │
│ (MyPy)   │   │(cov)   │   │  (cache) │
└──────────┘   └────────┘   └──────────┘
```

### 触发条件
- `push` 到 `main` / `develop` 分支
- `pull_request` 到 `main` 分支

### 本地预检

```bash
# 推荐在 push 前运行
make lint   # Ruff 检查
make format # 自动格式化
make test   # 确保测试通过
```

### Docker 镜像构建策略

- **多阶段构建** — 构建阶段安装编译依赖，运行阶段仅保留 FFmpeg
- **非 root 运行** — 安全最佳实践
- **HEALTHCHECK** — Docker 原生健康检查
- **Layer 缓存** — 利用 GitHub Actions cache 加速构建

---

## ⚙️ 运维指南

### 常用操作

```bash
# 查看所有服务状态
docker compose -f deploy/docker-compose.yml --profile prod ps

# 实时日志
docker compose -f deploy/docker-compose.yml --profile prod logs -f

# 重启特定服务
docker compose -f deploy/docker-compose.yml --profile prod restart api

# 查看资源使用
docker stats

# 备份数据
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### 更新部署

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建并重启
docker compose -f deploy/docker-compose.yml --profile prod up -d --build

# 3. 验证健康
curl https://your-domain.com/api/v1/health
```

### 监控建议

| 指标 | 工具 |
|------|------|
| API 可用性 | UptimeRobot (免费) |
| API 延迟 | Grafana + Prometheus |
| 系统资源 | Netdata / htop |
| 日志聚合 | Docker logs + Loki |
| AI API 用量 | OpenAI Usage Dashboard |

---

## 🐛 故障排查

### 常见问题

**1. Docker 拒绝连接**
```bash
# 检查 Docker daemon
sudo systemctl status docker

# 权限修复
sudo usermod -aG docker $USER
# 重新登录生效
```

**2. Redis 连接失败**
```bash
docker logs reagent-redis
# 确认 redis 服务在 reagent-net 网络中
docker network inspect reagent-net
```

**3. AI API 超时**
```bash
# 检查环境变量
docker exec reagent-api env | grep REAGENT_OPENAI

# 检查网络连通
docker exec reagent-api curl -s https://api.openai.com
```

**4. FFmpeg 未找到**
```bash
# 在容器内检查
docker exec reagent-api which ffmpeg
docker exec reagent-api ffmpeg -version
```

**5. SSL 证书过期**
```bash
# 自动续期（certbot）
sudo certbot renew

# 手动检查
docker compose -f deploy/docker-compose.yml --profile prod exec nginx nginx -t
```

---

## 📁 文件说明

```
deploy/
├── Dockerfile           # 多阶段 Docker 构建
├── docker-compose.yml   # 编排配置（dev/prod 多 profile）
├── nginx.conf           # 生产 Nginx 反向代理配置
├── .env.dev             # 开发环境变量模板
├── .env.test            # 测试/预发布环境变量模板
├── .env.prod            # 生产环境变量模板
├── Makefile             # 便捷命令集合
└── README.md            # 本文件

.github/workflows/
└── ci.yml               # GitHub Actions CI 流水线

pyproject.toml           # 项目元数据 + Ruff/Pytest 配置
```

---

## ✅ 部署检查清单

### 开发环境
- [ ] Docker & Docker Compose 已安装
- [ ] `.env` 已从 `.env.dev` 复制并配置
- [ ] `make dev` 成功启动
- [ ] `curl localhost:8000/api/v1/health` 返回 200
- [ ] `make test` 全部通过
- [ ] `make lint` 无错误

### 生产环境
- [ ] 服务器安全加固（防火墙、SSH Key、Docker 非 root 运行）
- [ ] 域名 DNS 已指向服务器 IP
- [ ] SSL 证书已配置
- [ ] `.env` 已使用安全随机字符串作为 JWT_SECRET
- [ ] AI API Key 已配置有额度限制
- [ ] `make prod` 成功启动所有服务
- [ ] 健康检查 URL 正常
- [ ] 数据库备份策略已设置
- [ ] 监控已配置
- [ ] 日志轮转已配置
