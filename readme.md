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

#### Milvus Standalone Docker Setup

The project uses Milvus standalone mode with the following architecture:

- **Milvus Standalone**: Main vector database service (port 19530)
- **etcd**: Metadata storage and service discovery
- **MinIO**: Object storage for vector data and logs

**Docker Compose Services:**

1. **etcd Container**:
   - Image: `quay.io/coreos/etcd:v3.5.0`
   - Purpose: Stores Milvus metadata and handles service coordination
   - Data persistence: `./volumes/etcd`

2. **MinIO Container**:
   - Image: `minio/minio:RELEASE.2020-12-03T00-03-10Z`
   - Purpose: Object storage backend for vector data
   - Default credentials: `minioadmin/minioadmin`
   - Data persistence: `./volumes/minio`

3. **Milvus Standalone Container**:
   - Image: `milvusdb/milvus:latest
   - Purpose: Main vector database service
   - Port mapping: `19530:19530`
   - Data persistence: `./volumes/milvus`

**Volume Management:**
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs milvus-standalone

# Stop services
docker-compose down

# Remove volumes (WARNING: This deletes all data)
docker-compose down -v
```

**Connection Configuration:**
The application connects to Milvus using:
- Host: `localhost`
- Port: `19530`
- No authentication required in standalone mode

5. **Set up SQL Server database**

- Configure connection string in `src/setup.py`
- Database schema: `KNS_Description` with table `kns_members` containing columns: `KNS_name`, `kns_name_hebrew`, `description`, `knesset_seat`
- **Database CSV Import**:  
    A CSV file containing all the data required for the SQL Server database is available at `db_csv/final_db.csv`. You can use this file to import the necessary data into SSMS (SQL Server Management Studio).

## 🚀 Usage

### Populating Milvus Vector Database with Knesset Member Quotes

Before using the chat application, you need to populate the Milvus vector database with Knesset member quotes. The system provides functions to automatically retrieve quotes from Elasticsearch and insert them into Milvus collections.

#### Available Functions in `setup.py`:

1. **`get_data_into_milvus()`** - Creates separate collections for each Knesset member per Knesset number
   - Collection naming format: `{member_name}_{knesset_number}`
   - Example: `Benjamin_Netanyahu_25`, `Miri_Regev_24`

2. **`get_data_into_milvus_no_kns_num()`** - Creates single collections per member across all Knesset terms
   - Collection naming format: `{member_name}`
   - Example: `Benjamin_Netanyahu`, `Miri_Regev`

#### Running the Data Population:

```python
# In Python console or script:
from setup import get_data_into_milvus_no_kns_num

# Populate all member collections (recommended approach)
get_data_into_milvus_no_kns_num()
```

#### Data Flow Process:

1. **Retrieve Member Names**: Gets all Knesset member names from SQL Server database
2. **Fetch Quotes**: Uses `retrieve_quotes_of_KNS_member()` to get quotes from Elasticsearch
3. **Clean Text**: Filters Hebrew text and removes sentences shorter than 30 characters
4. **Generate Embeddings**: Creates vector embeddings using multilingual sentence transformer
5. **Store in Milvus**: Inserts quotes and embeddings into named collections

#### Collection Management:

```python
# Check if collection exists
from Milvus_db import collection_exists
if collection_exists("Benjamin_Netanyahu"):
    print("Collection exists")

# Delete collections if needed
from setup import delete_kns_collections_no_kns_num
delete_kns_collections_no_kns_num()
```

### Running the Chat Application

```bash
cd src/
streamlit run chat.py
```

## 🔧 Configuration

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
