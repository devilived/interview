import chromadb
from chromadb.config import Settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma")

client = chromadb.Client(
    Settings(persist_directory=CHROMA_DIR, anonymized_telemetry=False)
)

collection = client.get_or_create_collection(name="questions")


def add_question(
    question_id: int, question: str, answer: str, category: str, source: str
):
    text = f"Question: {question}\nAnswer: {answer}"
    collection.add(
        ids=[str(question_id)],
        documents=[text],
        metadatas=[
            {
                "category": category,
                "source": source,
                "question": question,
                "answer": answer,
            }
        ],
    )


def delete_question(question_id: int):
    collection.delete(ids=[str(question_id)])


def update_question(
    question_id: int, question: str, answer: str, category: str, source: str
):
    delete_question(question_id)
    add_question(question_id, question, answer, category, source)


def search_similar(query: str, n_results: int = 5):
    results = collection.query(query_texts=[query], n_results=n_results)
    return results
