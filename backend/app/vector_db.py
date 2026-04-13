"""
ChromaDB 向量数据库封装模块 - 用于存储和检索问题的向量嵌入
"""
import os
import chromadb

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")

os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
collection = client.get_or_create_collection(name="questions")


def add_question(question_id: int, question: str, answer: str, category: str, source: str):
    """
    添加问题到向量数据库

    Args:
        question_id: 问题ID (与SQLite主键一致)
        question: 问题文本
        answer: 答案文本
        category: 问题分类
        source: 问题来源
    """
    doc = f"{question} {answer}"
    collection.add(
        ids=[str(question_id)],
        documents=[doc],
        metadatas=[{
            "category": category,
            "source": source,
            "question": question,
            "answer": answer
        }]
    )


def delete_question(question_id: int):
    """
    从向量数据库删除问题

    Args:
        question_id: 问题ID
    """
    collection.delete(ids=[str(question_id)])


def update_question(question_id: int, question: str, answer: str, category: str, source: str):
    """
    更新向量数据库中的问题

    Args:
        question_id: 问题ID
        question: 问题文本
        answer: 答案文本
        category: 问题分类
        source: 问题来源
    """
    doc = f"{question} {answer}"
    collection.update(
        ids=[str(question_id)],
        documents=[doc],
        metadatas=[{
            "category": category,
            "source": source,
            "question": question,
            "answer": answer
        }]
    )


def search_questions(query: str, n_results: int = 5, category: str = None):
    """
    搜索相似问题

    Args:
        query: 搜索查询文本
        n_results: 返回结果数量
        category: 可选的分类过滤

    Returns:
        搜索结果列表
    """
    where_filter = {"category": category} if category else None
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter
    )
    return results
