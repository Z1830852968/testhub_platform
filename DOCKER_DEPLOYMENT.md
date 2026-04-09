# TestHub Docker 部署指南

## 快速开始

### 1. 环境准备

确保已安装：
- Docker (20.10+)
- Docker Compose (2.0+)

### 2. 配置环境变量

复制环境变量示例文件并修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件，**务必修改以下生产环境配置**：

```bash
# 安全配置（必须修改）
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 数据库配置
DB_NAME=testhub
DB_USER=testhub
DB_PASSWORD=strong-password-here

# Redis 密码（可选，建议设置）
REDIS_PASSWORD=your-redis-password
```

### 3. 启动服务

#### 开发环境（包含所有服务）：

```bash
docker-compose up -d
```

#### 生产环境（推荐）：

```bash
# 使用生产配置文件
docker-compose -f docker-compose.yml up -d
```

### 4. 查看服务状态

```bash
# 查看所有容器状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery
```

### 5. 访问应用

- **前端**: http://localhost (或配置的 FRONTEND_PORT)
- **后端 API**: http://localhost/api/
- **Admin**: httplocalhost/admin/

## 服务说明

| 服务 | 端口 | 说明 |
|------|------|------|
| frontend | 80 | Vue.js 前端 + Nginx |
| backend | 8000 | Django 后端 (Gunicorn) |
| db | 3306 | MySQL 数据库 |
| redis | 6379 | Redis 缓存 |
| celery | - | Celery 异步任务 worker |
| celery-beat | - | Celery 定时任务调度器 |

## 常用命令

### 启动/停止

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 停止并删除数据卷（谨慎使用！）
docker-compose down -v
```

### 重建镜像

```bash
# 重新构建所有服务
docker-compose build

# 强制重新构建（不使用缓存）
docker-compose build --no-cache
```

### 数据库操作

```bash
# 进入数据库容器
docker-compose exec db mysql -u testhub -p

# 创建迁移
docker-compose exec backend python manage.py makemigrations

# 执行迁移
docker-compose exec backend python manage.py migrate

# 创建超级用户
docker-compose exec backend python manage.py createsuperuser
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f celery

# 查看最近 100 行
docker-compose logs --tail=100 backend
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 进入数据库容器
docker-compose exec db bash
```

## 生产环境部署

### 1. 安全配置

- ✅ 设置强 SECRET_KEY
- ✅ 设置 DEBUG=False
- ✅ 配置 ALLOWED_HOSTS 为具体域名
- ✅ 使用强数据库密码
- ✅ 配置 HTTPS（需要反向代理）

### 2. 使用 Nginx 反向代理（推荐）

在宿主机配置 Nginx：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. HTTPS 配置

使用 Let's Encrypt：

```bash
# 安装 certbot
apt install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com
```

## 故障排查

### 常见问题

1. **容器无法启动**
   ```bash
   # 查看详细错误
   docker-compose logs backend
   
   # 检查端口占用
   netstat -tlnp | grep :8000
   ```

2. **数据库连接失败**
   ```bash
   # 等待数据库就绪
   docker-compose logs db
   
   # 重启数据库
   docker-compose restart db
   ```

3. **静态文件 404**
   ```bash
   # 重新收集静态文件
   docker-compose exec backend python manage.py collectstatic --noinput
   ```

4. **Celery 任务不执行**
   ```bash
   # 查看 Celery 日志
   docker-compose logs celery
   
   # 重启 Celery
   docker-compose restart celery
   ```

### 重置环境

```bash
# 停止并删除所有容器、网络
docker-compose down

# 删除数据卷（会丢失所有数据！）
docker volume rm workspace_mysql_data
docker volume rm workspace_redis_data

# 重新启动
docker-compose up -d
```

## 性能优化

### 1. 调整 Worker 数量

编辑 `docker-compose.yml`，修改 Gunicorn workers：

```yaml
command: gunicorn --bind 0.0.0.0:8000 --workers 8 backend.wsgi:application
```

建议：workers = (2 x CPU cores) + 1

### 2. 增加资源限制

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### 3. 使用外部数据库

修改 `.env`：

```bash
DB_HOST=your-external-db-host
```

## 备份与恢复

### 备份数据库

```bash
docker-compose exec db mysqldump -u testhub -p testhub > backup.sql
```

### 恢复数据库

```bash
docker-compose exec -T db mysql -u testhub -p testhub < backup.sql
```

## 更新部署

```bash
# 拉取最新代码
git pull

# 重建并重启
docker-compose build
docker-compose up -d

# 执行迁移
docker-compose exec backend python manage.py migrate
```
