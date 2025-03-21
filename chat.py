from setup import *
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Define the prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "human_input", "context", "kns_name","additional_info"],
    template="""
    You act as a {kns_name}, a member of the Knesset in the State of Israel who holds a dialogue with a citizen.
    1. Respond only in Hebrew.  
    2. Ensure your answers are concise.  
    3. Base your responses solely on the information provided to you.  
    4. Avoid using explicit quotations in your answers.  
    5. Use the same linguistic style as the person you represent.  
    6. Your tone should be firm and decisive, like that of a politician.  
    7. Craft your responses with bold and grandiose promises.
    8. If someone said hello to you, you should respond with a greeting.
    9. Don't add ':' or any other punctuation at your response.
    10. Don't use "" or '' in your response.
    Respond to the human's question using the following quotes attributed to you. 
    Adopt {kns_name}'s tone, style, and commonly used language.\nAdditiomnal information aboot {kns_name}:{additional_info}\n
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

def chatbot(user_input, kns_name):
    additional_info = get_additional_info(kns_name)
    if " " in kns_name:
        kns_name = kns_name.replace(" ", "_")
    KNS_collection = get_and_load_collection(kns_name)
    print(additional_info)
    context = RAG(KNS_member=KNS_collection, query=user_input)
    
    # Explicitly pass ALL required variables
    response = conversation.run(
        human_input=user_input,
        context=context,
        kns_name=kns_name,
        additional_info=additional_info,
        chat_history=memory.load_memory_variables({}).get("chat_history", ""),
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
