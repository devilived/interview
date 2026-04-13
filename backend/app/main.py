"""
FastAPI 主入口文件 - Agent 面试题管理系统
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import questions, resume

app = FastAPI(title="Agent 面试题管理系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)
app.include_router(resume.router)


@app.get("/")
def root():
    """根路径返回欢迎信息"""
    return {"message": "Agent 面试题管理系统 API"}


@app.get("/health")
def health():
    """健康检查端点"""
    return {"status": "ok"}
