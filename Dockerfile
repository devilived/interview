# Agent 面试题管理系统 - Docker 镜像
FROM python:3.11-slim

LABEL maintainer="Agent Interview System"
LABEL description="Agent 面试题管理系统 Docker 镜像"

WORKDIR /www/wwwroot/interview

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    vim \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY backend/ ./backend/
COPY frontend/ ./frontend/

RUN pip install --no-cache-dir -r backend/requirements.txt

RUN cd frontend && npm install && npm run build

RUN mkdir -p ./data && chmod -R 777 ./data

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DATABASE_URL=sqlite:///./data/interview.db
ENV CHROMA_PERSIST_DIR=/www/wwwroot/interview/data/chroma

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["sh", "-c", "pip install -r backend/requirements.txt && cp -r frontend/dist backend/app/static && mkdir -p data && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"]
