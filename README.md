# Agent 面试题管理系统

## 项目结构

```
.
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI 入口
│   │   ├── database.py     # SQLite 配置
│   │   ├── vector_db.py    # ChromaDB 封装
│   │   ├── chains.py       # LangChain Chains
│   │   ├── models.py       # Pydantic 模型
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── questions.py # 题库 API
│   │       └── resume.py   # 简历面试 API
│   ├── data/               # 数据存储
│   │   ├── interview.db    # SQLite 数据库
│   │   └── chroma/         # ChromaDB 存储
│   └── requirements.txt
├── frontend/               # 前端服务
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── api/
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
└── README.md
```

## 环境配置

### 后端

```bash
cd backend
pip install -r requirements.txt

# 创建数据目录
mkdir -p data/chroma

# 运行
python -m uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## API 文档

启动后访问: http://localhost:8000/docs

## Harness CI/CD

配置文件位于 `.harness/pipeline.yaml`