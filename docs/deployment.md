# 部署指南 (Deployment Guide)

本项目是一个成熟的 FastAPI 脚手架，推荐使用 **Docker** 和 **Docker Compose** 进行线上部署。

## 1. 快速部署 (Docker Compose)

推荐使用 Docker Compose 进行管理，支持一键切换环境。

### 1.1 准备环境文件
项目支持通过 `APP_ENV` 加载不同的配置文件（`.env.<env>`）。

1.  **生产环境** (Production):
    ```bash
    cp .env.example .env.production
    # 编辑 .env.production，填入生产数据库、Redis 和密钥信息
    ```

2.  **测试环境** (Test):
    ```bash
    cp .env.example .env.test
    # 编辑 .env.test
    ```

### 1.2 启动服务
通过 `APP_ENV` 环境变量指定要加载的配置：

```bash
# 启动生产环境 (默认加载 .env.production)
APP_ENV=production docker compose up -d

# 启动测试环境 (加载 .env.test)
APP_ENV=test docker compose up -d
```

## 2. 使用 Docker CLI 部署

对于 CI/CD 或简单场景，可以直接使用 Docker 命令。

### 2.1 构建镜像
```bash
docker build -t fastapi-app .
```

### 2.2 运行容器
使用 `-e` 参数传递环境配置和 Gunicorn 参数：

```bash
# 示例：运行测试环境，启动 8 个 Worker 进程
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  -e APP_ENV=test \
  -e GUNICORN_WORKERS=8 \
  fastapi-app
```

## 3. 高级配置 (Gunicorn)

可以通过环境变量动态调整 Gunicorn 的行为：

| 环境变量 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `GUNICORN_WORKERS` | `4` | Worker 进程数。建议设置为 `(CPU核心数 * 2) + 1`。 |
| `GUNICORN_BIND` | `0.0.0.0:8000` | Gunicorn 监听地址和端口。 |

### ⚠️ 注意：修改绑定端口
如果你修改了 `GUNICORN_BIND`（例如改为 `0.0.0.0:9000`），必须同步注意：

1.  **Docker 端口映射**：
    你需要将宿主机端口映射到**新的容器端口**。
    ```bash
    # 正确示例：映射到容器的 9000 端口
    docker run -p 8000:9000 ...
    ```

2.  **健康检查 (Healthcheck)**：
    `Dockerfile` 中的健康检查默认探测 `http://localhost:8000/health`。
    如果端口变更，你需要覆盖健康检查命令，否则容器会一直显示 `unhealthy`。

## 4. 生产环境配置建议

### 4.1 环境变量 (.env)
在线上环境，请务必修改以下配置：
- `SECRET_KEY`: 生成一个强随机字符串。
- `PROJECT_NAME`: 你的项目名称。

### 4.2 反向代理 (Nginx)

强烈建议在 Docker 容器前加一层 Nginx 作为反向代理，用于处理 HTTPS、静态资源和负载均衡。

**Nginx 示例配置：**
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 5. 数据库迁移

1.  **自动执行**：
    `docker-compose.yml` 中的 `command` 或者 entrypoint 脚本通常会包含 `alembic upgrade head`，容器启动时自动迁移。

2.  **手动执行**：
    如果需要手动运行迁移命令：
    ```bash
    docker compose exec app alembic upgrade head
    ```

## 6. 日志管理

项目使用标准输出 (stdout) 记录日志，你可以通过 Docker 命令查看：

```bash
# 实时查看日志
docker logs -f <container_name>
```

建议配合 EFK (Elasticsearch, Fluentd, Kibana) 或类似的工具进行日志收集。

## 7. CI/CD 集成建议

推荐使用 GitHub Actions 或 GitLab CI 实现自动化部署：
1.  **Checkout 代码**
2.  **运行测试** (pytest)
3.  **构建 Docker 镜像**
4.  **推送到镜像仓库**
5.  **SSH 远程执行部署脚本** (docker pull & docker up)
