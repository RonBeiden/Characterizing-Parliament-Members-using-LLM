# Characterizing Parliament Members using LLM

## Overview

This project leverages Large Language Models (LLMs) to analyze and characterize Israeli Knesset (Parliament) members based on their speeches, voting patterns, and public statements. The system uses advanced Retrieval-Augmented Generation (RAG) techniques, embeddings, and vector databases to create AI personas that can respond in the style and voice of specific politicians, particularly focusing on members like Miri Regev and Benjamin Netanyahu.

## 🚀 Key Features

### Core Functionality

- **Parliamentary Data Analysis**: Processes speeches, quotes, and voting records from the Israeli Knesset
- **AI Persona Generation**: Creates chatbots that mimic specific politicians' communication styles
- **Multilingual Support**: Handles Hebrew text processing and generation
- **Real-time Conversations**: Interactive chat interface with memory and context awareness

### Technical Components

- **Vector Search**: Uses Milvus vector database for efficient similarity search across political statements
- **Multiple Embedding Models**: Supports various sentence transformers (MiniLM, E5, XLM-RoBERTa)
- **RAG Pipeline**: Retrieval-Augmented Generation for contextually relevant responses
- **Conversation Memory**: Maintains chat history and context using LangChain
- **External Knowledge**: Integration with Tavily for real-time web search capabilities

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Processing     │    │   AI Models     │
│                 │    │                  │    │                 │
│ • Knesset DB    │───▶│ • Text Cleaning  │───▶│ • OpenAI GPT-4  │
│ • Speech Data   │    │ • Embeddings     │    │ • Ollama (Local)│
│ • Voting Records│    │ • Vector Storage │    │ • Sentence Trans│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Vector DB      │    │   Evaluation    │
│                 │    │                  │    │                 │
│ • Streamlit UI  │◄───│ • Milvus         │    │ • Similarity    │
│ • Chat Interface│    │ • Elasticsearch  │    │ • Vote Analysis │
│ • Jupyter NB    │    │ • Collections    │    │ • Model Compare │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
Characterizing-Parliament-Members-using-LLM/
├── src/                          # Core application code
│   ├── chat.py                   # Main chat interface and logic
│   ├── setup.py                  # Configuration and utilities
│   └── Milvus_db.py             # Vector database operations
├── notebooks/                    # Jupyter notebooks for development
│   ├── RAG.ipynb                # RAG pipeline implementation
│   ├── vector_db.ipynb          # Vector database experiments
│   ├── MiILVUS.ipynb           # Milvus integration
│   ├── description_data.ipynb   # Data processing
│   ├── answers_similarity.ipynb # Evaluation metrics
│   └── Taviliy_playground.ipynb # External search integration
├── eval/                        # Evaluation and testing
│   ├── notebooks/               # Evaluation notebooks
│   │   ├── embading_compare.ipynb    # Embedding model comparison
│   │   ├── embading_test.ipynb       # Embedding testing
│   │   ├── votes_mk.ipynb            # Voting analysis
│   │   └── knesset_votes_demo.ipynb  # Vote matching demo
│   └── laws/                    # Legal documents for context
├── const/                       # Constants and data files
├── db_csv/                      # Database CSV exports
├── volumes/                     # Docker volumes
├── milvus_data/                 # Milvus database files
└── requirements.txt             # Python dependencies
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- SQL Server (for Knesset database)
- Milvus vector database

### Installation Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd Characterizing-Parliament-Members-using-LLM
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_openai_key
# TAVILY_API_KEY=your_tavily_key
```

4. **Start Milvus database**

```bash
docker-compose up -d
```

5. **Set up SQL Server database**

- Configure connection string in `src/setup.py`

## 🚀 Usage

### Running the Chat Application

```bash
cd src/
streamlit run chat.py
```

## 🔧 Configuration

### Supported Politicians

- **Miri Regev**: Israeli politician, former Culture Minister
- **Benjamin Netanyahu**: Israeli Prime Minister
- **Extensible**: Add new politicians by processing their speech data

### Embedding Models

- `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensions)
- `intfloat/multilingual-e5-large` (1024 dimensions)
- `XLM-RoBERTa` (768 dimensions)

### LLM Models

- **OpenAI GPT-4o-mini**: Primary generation model
- **Ollama**: Local models (Mistral, Llama, Phi)

## 📊 Evaluation

The project includes comprehensive evaluation mechanisms:

### Similarity Analysis

- **[answers_similarity.ipynb](notebooks/answers_similarity.ipynb)**: Compare generated vs. real responses
- Semantic similarity using sentence transformers

### Voting Pattern Analysis

- **[votes_mk.ipynb](eval/notebooks/votes_mk.ipynb)**: Analyze voting consistency
- **[knesset_votes_demo.ipynb](eval/notebooks/knesset_votes_demo.ipynb)**: Vote prediction accuracy

### Model Comparison

- **[embading_compare.ipynb](eval/notebooks/embading_compare.ipynb)**: Compare embedding models
- Performance metrics across different similarity tasks

## 🎯 Example Queries

```python
# Hebrew query examples:
"מה דעתך על תחבורה ציבורית בישראל?"
"איך אתה רואה את מצב הביטחון?"
```

## 🔍 Key Functions

### [`chat.py`](src/chat.py)

- Main conversation logic
- Query rephrasing and context management
- Integration with vector search and LLM generation

### [`setup.py`](src/setup.py)

- Database
