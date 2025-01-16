from setup import *
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Define the prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "human_input", "context", "kns_name"],
    template="""You are {kns_name}, a member of the Israeli Knesset. 
    Respond to the human's question using the following quotes attributed to you. 
    Adopt {kns_name}'s tone, style, and commonly used language:\n
    Context: {context}\n\nChat History: {chat_history}\n\nHuman: {human_input}\nAI:"""
)

# Memory configuration
memory = ConversationBufferMemory(input_key="human_input", memory_key="chat_history")

# Define the ConversationChain
conversation = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True  # Add verbose for debugging
)

def chatbot(user_input):
    context = RAG(KNS_member=KNS_collection, query=user_input)
    
    # Explicitly pass ALL required variables
    response = conversation.run(
        human_input=user_input,
        context=context,
        kns_name=kns_name,
        chat_history=memory.load_memory_variables({}).get("chat_history", "")
    )
    
    memory.save_context({"human_input": user_input}, {"output": response})
    return response

# Summarize conversation function
def summarize_conversation(conversation):
    summary_prompt = f"Summarize the following conversation in a concise manner:\n\n{conversation}\n\nSummary:"
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=summary_prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
