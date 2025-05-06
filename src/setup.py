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

def get_knesset_numbers(kns_name):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-9LFS960\SQLEXPRESS;'
        'DATABASE=KNS_Description;'
        'Trusted_Connection=yes'
    )
    cursor = conn.cursor()
    query = "SELECT knesset_seat FROM kns_members WHERE kns_name = ?"
    cursor.execute(query, kns_name)
    seats = [row[0] for row in cursor.fetchall()]
    result = [int(x) for x in seats[0].split(',')]
    conn.close()
    return result

def get_kns_names_and_hebrew():
  conn = pyodbc.connect(
      'DRIVER={ODBC Driver 17 for SQL Server};'
      'SERVER=DESKTOP-9LFS960\SQLEXPRESS;'
      'DATABASE=KNS_Description;'
      'Trusted_Connection=yes'
  )
  cursor = conn.cursor()
  query = "SELECT kns_name, kns_name_hebrew FROM kns_members"
  cursor.execute(query)
  names = []
  names_hebrew = []
  for row in cursor.fetchall():
    names.append(row[0])
    names_hebrew.append(row[1])
  conn.close()
  return names, names_hebrew

def get_data_into_milvus():
    names, names_hebrew = get_kns_names_and_hebrew()
    print(f"Names: {names}")
    for name, name_hebrew in zip(names, names_hebrew):
        print(f"Processing {name}...")
        kns_numbers = get_knesset_numbers(name)
        if " " in name:
            kns_name = name.replace(" ", "_")
        for kns_number in kns_numbers:
            print(f"Processing {name_hebrew} in Knesset {kns_number}...")
            quotes = retrieve_quotes_of_KNS_member(name_hebrew, knesset_number=kns_number)
            if not quotes:
                continue
            else:
                collection = vector_db(quotes, collection_name=f"{kns_name}_{kns_number}")
            print(f"Collection {kns_name}_{kns_number} created successfully.")

# if __name__ == '__main__':
#     get_data_into_milvus()