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
import pyodbc
load_dotenv()

# Initialize OpenAI API (replace with your API key)
key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain components
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=key)

memory = ConversationBufferMemory(memory_key="chat_history")

# get additional information about the KNS member
def get_additional_info(kns_name):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=DESKTOP-9LFS960\SQLEXPRESS;'
                          'DATABASE=KNS_Description;'
                          'Trusted_Connection=yes')
    cursor = conn.cursor()
    query = "SELECT [Description] FROM kns_history WHERE KNS_name = ?"
    cursor.execute(query, kns_name)
    rows = cursor.fetchall()
    descriptions = [row[0] for row in rows]  
    conn.close()
    return descriptions

