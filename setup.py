import streamlit as st
from sentence_transformers import SentenceTransformer
import openai
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from langchain.chat_models import ChatOpenAI
from Milvus_db import *
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI API (replace with your API key)
key = os.getenv("OPENAI_API_KEY")
print(key)
# # Initialize LangChain components
# llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=key)

# memory = ConversationBufferMemory(memory_key="chat_history")

# # Knowledge source name (replace with your actual knowledge source)
# kns_name = "Miri_Regev"
# KNS_collection = get_and_load_collection(kns_name)

