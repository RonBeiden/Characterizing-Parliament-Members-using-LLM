from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
from sentence_transformers import SentenceTransformer
import os
from elasticsearch import Elasticsearch
import re

elastic_ip = '34.0.64.248:9200'
kibana_ip = '34.0.64.248:5601'
es_username = 'user'
es_password = 'knesset'

#load_dotenv()
milvus_host = "localhost"
milvus_port = 19530
connections.connect("default", host=milvus_host, port=milvus_port)

# Check the model output dimension
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
dimension = model.get_sentence_embedding_dimension()

def vector_db(docs, collection_name="demo"):
    # Drop the collection if it exists
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=500)  # Adding content field for storage
    ]

    schema = CollectionSchema(fields=fields, enable_dynamic_field=True)
    demo = Collection(collection_name, schema=schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 128}
    }

    demo.create_index(
        field_name="vector",
        index_params=index_params
    )

    ids = []
    vectors = []
    contents = []
    for i, doc in enumerate(docs):
        if isinstance(doc, str):
            text_content = doc  # Directly use the document content if it's already a string
        else:
            text_content = doc.page_content  # Assuming doc has a 'page_content' attribute or similar
        
        embeddings = model.encode(text_content)
        vector = embeddings.tolist()
        ids.append(i)
        vectors.append(vector)
        contents.append(text_content)  # Store the document content
       # print(f"Document {i}: {text_content}")
       # print(f"Vector: {vector[:5]}...")  # Print first 5 dimensions for brevity

    # Insert the data as separate lists for each field
    demo.insert([ids, vectors, contents])

    return demo

    # Return a callable retriever
def retriever(query, demo):
    if isinstance(query, dict) and 'question' in query:
        query = query['question']
    elif not isinstance(query, str):
        raise ValueError(f"Unexpected query format: {query}")

    # Encode the query and perform a search on the collection
    query_embedding = model.encode(query).tolist()
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    results = demo.search([query_embedding], "vector", param=search_params, limit=20, output_fields=["id", "content"])
    
    # Check search results
    #print("Search results:", results)
    
    # Fetch detailed content of the results
    search_results = []
    if results:
        for result in results[0]:
            entity = demo.query(expr=f"id == {result.id}", output_fields=["id", "content"])
            if entity:
                search_results.append(entity[0]['content'])
            #print(f"Entity for id {result.id}:", entity)

    return search_results



def retrive_quotes(KNS_name):

    es = Elasticsearch(f'http://{elastic_ip}', basic_auth=(es_username, es_password), request_timeout=500)
    data_q =[]
    # Query definition
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"speaker_name": KNS_name}}
                ],
                "filter": {
                    "script": {
                        "script": {
                            "source": "doc['sentence_text.keyword'].size() > 0 && doc['sentence_text.keyword'].value.length() > 30"
                        }
                    }
                }
            }
        }
    }

    # Initialize scroll
    resp = es.search(index="all_features_sentences", body=query, scroll="2m", size=1000)

    # Retrieve the scroll ID and first batch of hits
    scroll_id = resp['_scroll_id']
    hits = resp['hits']['hits']

    total_hits = 0
    while total_hits<4000:
        for hit in hits:
            data_q.append("%(sentence_text)s" % hit["_source"])
        #print("%(sentence_text)s" % hit["_source"])

        total_hits += len(hits)

        # Fetch the next batch
        resp = es.scroll(scroll_id=scroll_id, scroll="2m")
        scroll_id = resp['_scroll_id']
        hits = resp['hits']['hits']

    print(f"Total results retrieved: {total_hits}")

    # Clear the scroll to free resources
    es.clear_scroll(scroll_id=scroll_id)
    for i in range(len(data_q)):
        data_q[i] = re.sub(r'[^א-ת ]', '', data_q[i]).strip()

    return data_q


def retrieve_quotes_of_KNS_member(name):
    data = retrive_quotes(name)
    return data

def get_and_load_collection(name):
    KNS_member = Collection(name)
    KNS_member.load()
    return KNS_member

def RAG(KNS_member, query):
    results = retriever(query, KNS_member)
    return results

# vector_db(retrieve_quotes_of_KNS_member('מירי רגב'), 'Miri_Regev')