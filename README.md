# 📚 Smart Librarian

**Smart Librarian** is an AI-powered assistant that recommends books based on natural language input. It uses OpenAI's GPT for theme extraction and reasoning, ChromaDB for semantic search (RAG), and a local JSON file for full book summaries. A clean, responsive web UI is built using **Gradio**, with custom theming.

---

## ✅ Features

- Book recommendations via natural language
- GPT-powered theme extraction
- RAG pipeline with ChromaDB + OpenAI embeddings
- Full summaries loaded from local JSON (`book_summaries.json`)
- Modern Gradio web interface with custom theme and fonts

---

## 📁 Project Structure

smart_librarian/
├── chatbot/
│ ├── chatbot.py # GPT prompt logic
│ └── retriever.py # ChromaDB retriever
├── tools/
│ └── summaries.py # Loads summaries from JSON
├── data/
│ └── book_summaries.json # Local summary database
├── main.py # Optional CLI app
└── README.md



## ⚙️ Setup & Build Steps

### Clone the repository

git clone https://github.com/your-username/smart-librarian.git
cd smart-librarian

### Create and activate a virtual environment

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

### Set up your OpenAI API key
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx     # On Linux/macOS
set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx         # On Windows CMD

### Run the App
python ui/gradio_app.py
Then open your browser to:
http://localhost:7860


### Dependencies
openai
chromadb
gradio
tqdm



