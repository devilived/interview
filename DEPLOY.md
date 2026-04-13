# GitHub Secrets 配置指南

推送到 GitHub 之前，需要在 GitHub 仓库设置以下 Secrets：

## 需要配置的 Secrets

| Secret 名称 | 说明 | 你的配置 |
|-------------|------|----------|
| `SERVER_HOST` | 服务器 IP | `39.105.230.136` |
| `SERVER_PORT` | SSH 端口 | `9999` |
| `SERVER_USER` | 服务器用户名 | `root` |
| `SERVER_PASSWORD` | 服务器密码 | 你的密码 |

**注意**：`GITHUB_TOKEN` 是 GitHub 自动提供的，不需要手动创建。

## 配置步骤

### 1. 创建 GitHub 仓库并推送代码

```bash
cd E:\workspace-vs\ai
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/interview-system.git
git push -u origin main
```

### 2. 在 GitHub 仓库添加 Secrets

进入 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下 Secrets：

| Secret 名称 | 值 |
|-------------|-----|
| `SERVER_HOST` | `39.105.230.136` |
| `SERVER_PORT` | `9999` |
| `SERVER_USER` | `root` |
| `SERVER_PASSWORD` | 你的服务器密码 |

### 3. 服务器准备工作

在服务器上执行：
```bash
mkdir -p /www/wwwroot/interview/data
```

### 4. 宝塔防火墙放行端口

- `9999` (SSH)
- `8000` (应用)

### 5. 触发自动部署

推送到 main 分支：
```bash
git push origin main
```

之后每次推送到 main 分支都会自动构建并部署。

## 工作流说明

每次推送到 main 分支会自动：
1. 构建 Docker 镜像
2. 推送到 GitHub Container Registry (`ghcr.io`)
3. SSH 连接到服务器
4. 拉取最新镜像并重启容器

## 常用命令

```bash
# 查看容器日志
docker logs -f interview

# 重启应用
docker restart interview

# 停止应用
docker stop interview

# 查看容器状态
docker ps
```
