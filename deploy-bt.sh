#!/bin/bash
# ===========================================
# Agent 面试题管理系统 - 宝塔面板一键部署脚本
# ===========================================

set -e

# 配置
APP_NAME="interview"
APP_PORT=8000
APP_DIR="/www/wwwroot/${APP_NAME}"
DATA_DIR="${APP_DIR}/data"
REPO_URL="https://github.com/your-repo/interview-system.git"  # 修改为你的仓库地址

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    log_warn "请使用 sudo 或 root 用户运行此脚本"
    exit 1
fi

echo "=========================================="
echo "  Agent 面试题管理系统 - 宝塔部署脚本"
echo "=========================================="
echo ""

# 1. 检查 Docker
log_info "检查 Docker 环境..."
if ! command -v docker &> /dev/null; then
    log_error "Docker 未安装，正在安装..."
    curl -fsSL https://get.docker.com | sh
    systemctl start docker
    systemctl enable docker
    log_info "Docker 安装完成"
else
    log_info "Docker 已安装: $(docker --version)"
fi

# 2. 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log_warn "Docker Compose 未安装，尝试安装..."
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# 3. 创建目录
log_info "创建应用目录..."
mkdir -p ${APP_DIR}
mkdir -p ${DATA_DIR}

# 4. 复制项目文件
log_info "请将项目文件复制到: ${APP_DIR}"
log_info "或者修改脚本中的 REPO_URL 使用 git clone"

# 5. 创建 .env 文件
ENV_FILE="${APP_DIR}/.env"
if [ ! -f "${ENV_FILE}" ]; then
    log_info "创建环境配置文件..."
    cat > ${ENV_FILE} << 'EOF'
# LLM 配置
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://ark.cn-east-1.xfwd.xfounder.com/v1
OPENAI_MODEL=deepseek-v3-2-251201
OPENAI_MAX_TOKENS=8192
OPENAI_TEMPERATURE=0.6
EOF
    log_warn "请编辑 ${ENV_FILE} 填写你的 API Key"
else
    log_info ".env 文件已存在"
fi

# 6. 构建 Docker 镜像
log_info "构建 Docker 镜像..."
cd ${APP_DIR}
docker build -t ${APP_NAME} .

# 7. 停止旧容器（如果存在）
log_info "停止旧容器..."
docker stop ${APP_NAME} 2>/dev/null || true
docker rm ${APP_NAME} 2>/dev/null || true

# 8. 运行新容器
log_info "启动容器..."
docker run -d \
    --name ${APP_NAME} \
    -p ${APP_PORT}:8000 \
    --env-file ${ENV_FILE} \
    -v ${DATA_DIR}:/www/wwwroot/interview/data \
    --restart unless-stopped \
    ${APP_NAME}

# 9. 检查容器状态
sleep 3
if docker ps | grep -q ${APP_NAME}; then
    log_info "容器启动成功!"
    log_info "访问地址: http://你的服务器IP:${APP_PORT}"
else
    log_error "容器启动失败，请检查日志:"
    docker logs ${APP_NAME}
    exit 1
fi

echo ""
echo "=========================================="
log_info "部署完成!"
echo "=========================================="
echo ""
echo "常用命令:"
echo "  查看日志: docker logs -f ${APP_NAME}"
echo "  重启应用: docker restart ${APP_NAME}"
echo "  停止应用: docker stop ${APP_NAME}"
echo "  重新部署: cd ${APP_DIR} && docker-compose up -d --build"
echo ""
