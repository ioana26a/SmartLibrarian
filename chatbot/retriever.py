import os
import json
import chromadb
from chromadb.utils import embedding_functions

# Setarea cheii OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 1. Încarcă datele
def load_data(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fișierul '{file_path}' nu a fost găsit.")
    except json.JSONDecodeError:
        raise ValueError(f"Fișierul '{file_path}' nu este un JSON valid.")

# 2. Creează colecția și încarcă datele în ChromaDB
def create_collection(data: dict):
    titles = list(data.keys())
    texts = [data[title]["summary"] for title in titles]  # Extrage doar rezumatul
    collection = client.create_collection(
        name="books",
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )
    collection.add(
        documents=texts,
        ids=titles,
        metadatas=[{"title": t, "themes": ", ".join(data[t]["themes"])} for t in titles]  # Transformă lista în string
    )
    return collection

# 3. Funcție de căutare semantică
def search_books_by_theme(query: str, top_k: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results

# Încărcarea datelor și crearea colecției
summaries = load_data("data/book_summaries.json")
client = chromadb.Client()
collection = create_collection(summaries)

