"""
SQLite 数据库配置模块 - 使用 SQLAlchemy 进行数据库操作
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/interview.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Question(Base):
    """面试题数据库模型"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    source = Column(String(20), default="system")
    resume_id = Column(String(50))
    is_favorited = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db():
    """
    获取数据库会话的依赖函数

    Yields:
        数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库，创建所有表"""
    db_path = "./data/interview.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    Base.metadata.create_all(bind=engine)
