"""
FastAPI 主入口文件 - Agent 面试题管理系统
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from .routers import questions, resume

app = FastAPI(title="Agent 面试题管理系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)
app.include_router(resume.router)

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")


@app.get("/")
def root():
    """根路径返回前端页面"""
    index_path = os.path.join(STATIC_PATH, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Agent 面试题管理系统 API"}


@app.get("/health")
def health():
    """健康检查端点"""
    return {"status": "ok"}
