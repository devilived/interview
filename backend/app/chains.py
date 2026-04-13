"""
LangChain Chains 模块 - 负责与 LLM 交互生成面试题
"""
import os
import re
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "deepseek-v3-2-251201"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"),
    max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "8192")),
    temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.6")),
)

CATEGORY_PROMPTS = {
    "Agent": """你是一个资深的AI工程师面试官。请生成5个关于Agent开发的高质量面试题及详细答案。
要求：
- 问题涵盖Agent概念、架构设计、实践应用
- 答案详细、包含代码示例最佳
- 格式：每个问题以"问题1:"开头，每个答案以"答案1:"开头""",
    "RAG": """你是一个资深的AI工程师面试官。请生成5个关于RAG (Retrieval Augmented Generation) 开发的高质量面试题及详细答案。
要求：
- 问题涵盖RAG原理、向量检索、知识库构建
- 答案详细、包含代码示例最佳
- 格式：每个问题以"问题1:"开头，每个答案以"答案1:"开头""",
    "Memory": """你是一个资深的AI工程师面试官。请生成5个关于AI Memory (记忆机制) 开发的高质量面试题及详细答案。
要求：
- 问题涵盖短期记忆、长期记忆、记忆检索
- 答案详细、包含代码示例最佳
- 格式：每个问题以"问题1:"开头，每个答案以"答案1:"开头""",
    "Tool Calling": """你是一个资深的AI工程师面试官。请生成5个关于Tool Calling (工具调用) 开发的高质量面试题及详细答案。
要求：
- 问题涵盖工具定义、调用链、工具注册
- 答案详细、包含代码示例最佳
- 格式：每个问题以"问题1:"开头，每个答案以"答案1:"开头""",
}


def parse_qa_content(content: str) -> list:
    """
    解析问答内容

    Args:
        content: LLM返回的原始内容

    Returns:
        包含 question 和 answer 的字典列表
    """
    questions = []
    parts = re.split(r'(?=问题\d*[：:])', content)

    for part in parts:
        part = part.strip()
        if not part or not re.match(r'问题\d*[：:]', part):
            continue

        q_match = re.search(r'问题\d*[：:]\s*(.+?)(?=答案\d*[：:]|$)', part, re.DOTALL)
        a_match = re.search(r'答案\d*[：:]\s*(.+)', part, re.DOTALL)

        if q_match and a_match:
            question = q_match.group(1).strip()
            answer = a_match.group(1).strip()
            question = re.sub(r'\s+', ' ', question)
            answer = re.sub(r'\s+', ' ', answer)
            questions.append({"question": question, "answer": answer})

    return questions


def generate_questions(category: str, count: int = 5) -> list:
    """
    根据分类生成面试问题

    Args:
        category: 问题分类 (Agent/RAG/Memory/Tool Calling)
        count: 生成问题数量

    Returns:
        包含 question 和 answer 的字典列表
    """
    prompt = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["Agent"])
    prompt += f'\n\n请生成恰好{count}个问题。'

    response = llm.invoke(prompt)
    content = response.content

    questions = parse_qa_content(content)
    return questions[:count]


def generate_resume_questions(
    project_description: str, count: int = 3, history: list = None
) -> list:
    """
    根据项目描述生成面试问题

    Args:
        project_description: 项目描述文本
        count: 生成问题数量
        history: 已生成的问题历史

    Returns:
        包含 question 和 answer 的字典列表
    """
    history_context = ""
    if history:
        history_context = "\n已生成的问题：\n" + "\n".join(
            [f"- {h['question']}" for h in history]
        )

    prompt = f"""你是一个资深的AI工程师面试官。用户提供了项目描述，请生成{count}个针对性的面试题及详细答案。

项目描述：
{project_description}
{history_context}

要求：
- 问题基于项目技术栈进行深挖或扩展
- 答案详细、结合项目场景
- 格式：每个问题以"问题1:"开头，每个答案以"答案1:"开头"""

    response = llm.invoke(prompt)
    content = response.content

    questions = parse_qa_content(content)
    return questions[:count]


def regenerate_answer(question: str, category: str = "Agent") -> str:
    """
    重新生成某个问题的答案

    Args:
        question: 问题文本
        category: 问题分类

    Returns:
        生成的新答案
    """
    prompt = f"""你是一个资深的AI工程师面试官。请为以下问题生成更好的答案。

分类：{category}
问题：{question}

要求：
- 答案详细、包含代码示例最佳
- 格式：直接给出答案"""

    response = llm.invoke(prompt)
    return response.content
