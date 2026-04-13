import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY", "sk-dummy"),
    openai_api_base=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)

CATEGORY_PROMPTS = {
    "Agent": """你是一个资深的AI工程师面试官。请生成5个关于Agent开发的高质量面试题及详细答案。
要求：
- 问题涵盖Agent概念、架构设计、实践应用
- 答案详细、包含代码示例最佳
- 格式：问题+答案""",
    "RAG": """你是一个资深的AI工程师面试官。请生成5个关于RAG (Retrieval Augmented Generation) 开发的高质量面试题及详细答案。
要求：
- 问题涵盖RAG原理、向量检索、知识库构建
- 答案详细、包含代码示例最佳
- 格式：问题+答案""",
    "Memory": """你是一个资深的AI工程师面试官。请生成5个关于AI Memory (记忆机制) 开发的高质量面试题及详细答案。
要求：
- 问题涵盖短期记忆、长期记忆、记忆检索
- 答案详细、包含代码示例最佳
- 格式：问题+答案""",
    "Tool Calling": """你是一个资深的AI工程师面试官。请生成5个关于Tool Calling (工具调用) 开发的高质量面试题及详细答案。
要求：
- 问题涵盖工具定义、调用链、工具注册
- 答案详细、包含代码示例最佳
- 格式：问题+答案""",
}


def generate_questions(category: str, count: int = 5) -> list:
    prompt = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["Agent"])
    prompt += f"\n\n请生成恰好{count}个问题。"

    response = llm.invoke(prompt)
    content = response.content

    questions = []
    lines = content.split("\n")
    current_q = None
    current_a = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith(
            ("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")
        ):
            if current_q:
                questions.append(
                    {"question": current_q, "answer": "\n".join(current_a)}
                )
            current_q = line.split(".", 1)[1].strip()
            current_a = []
        elif (
            line.startswith("答案:") or line.startswith("A:") or line.startswith("答:")
        ):
            current_a.append(line.split(":", 1)[1].strip() if ":" in line else line)
        elif current_q and current_a:
            current_a.append(line)

    if current_q:
        questions.append({"question": current_q, "answer": "\n".join(current_a)})

    return questions[:count]


def generate_resume_questions(
    project_description: str, count: int = 3, history: list = None
) -> list:
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
- 格式：问题+答案"""

    response = llm.invoke(prompt)
    content = response.content

    questions = []
    lines = content.split("\n")
    current_q = None
    current_a = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith(("1.", "2.", "3.", "4.", "5.")):
            if current_q:
                questions.append(
                    {"question": current_q, "answer": "\n".join(current_a)}
                )
            current_q = line.split(".", 1)[1].strip()
            current_a = []
        elif current_q and current_a:
            current_a.append(line)

    if current_q:
        questions.append({"question": current_q, "answer": "\n".join(current_a)})

    return questions[:count]


def regenerate_answer(question: str, category: str = "Agent") -> str:
    prompt = f"""你是一个资深的AI工程师面试官。请为以下问题生成更好的答案。

分类：{category}
问题：{question}

要求：
- 答案详细、包含代码示例最佳
- 格式：直接给出答案"""

    response = llm.invoke(prompt)
    return response.content
