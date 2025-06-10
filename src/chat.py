from setup import *
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from tavily import TavilyClient

Rephrase_prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context", "kns_name"],
        template="""
        You are tasked with rephrasing a user's query to ensure it is clear, concise, and includes all necessary context for another LLM to understand.
        add the name of the Knesset member to the rephrased query, like a user asked a question to the Knesset member.
        for example: "What is your opinion on the new law?" should be rephrased to "What is the opinion of {kns_name} on the new law?".

        Follow these guidelines:
        1. Maintain the original intent of the user's query.  
        3. Ensure the rephrased query is in Hebrew.  
        4. Avoid adding any unnecessary details or assumptions.  
        5. Use a formal and professional tone.
        
        VERY IMPORTANT: If the user asked answer בעד או נגד. Don't add it to the rephrased query!! delete it from the rephrased query.

        Context: {context}  
        The Knesset member name: {kns_name}
        Chat History: {chat_history}  

        Original Query: {human_input}  
        Rephrased Query:"""
    )
  
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
    11. Don't mention any time or date in your response, event no time related words like 'today', 'now', 'tomorrow', 'after holidays' etc.
    12. If the user asks about your stance on a specific law, respond decisively with either support or opposition.
    13. If the user asks about your opinion on a specific law, respond with a clear and concise opinion.   
    Respond to the human's question using the following quotes attributed to you. 
    Adopt {kns_name}'s tone, style, and commonly used language.\nAdditiomnal information aboot {kns_name}:{additional_info}\n
    \n\n
    Context: {context}\n\nChat History: {chat_history}\n\nHuman: {human_input}\nAI:"""
)

# Memory configuration
memory = ConversationBufferMemory(input_key="human_input", memory_key="chat_history")

conversation_for_Tavily = LLMChain(
    llm=llm,
    memory=memory,
    prompt=Rephrase_prompt,
    verbose=True  # Add verbose for debugging
)
# Define the ConversationChain
conversation = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True  # Add verbose for debugging
)

def chatbot(user_input, kns_name):
    if " " in kns_name:
        kns_name = kns_name.replace(" ", "_")
    print("Getting KNS collection...")
    KNS_collection = get_and_load_collection(kns_name)
    print("Got KNS collection")
    if kns_name[-1].isdigit():
        kns_name = kns_name[:-3]
    if '_' in kns_name:
        kns_name = kns_name.replace("_", " ")
    print(kns_name)
    additional_info = get_additional_info(kns_name)
    print(additional_info)
    context = RAG(KNS_member=KNS_collection, query=user_input)
    

    question_for_tavily = conversation_for_Tavily.run(
        human_input=user_input,
        context=context,
        kns_name=kns_name,
        additional_info=additional_info,
        chat_history=memory.load_memory_variables({}).get("chat_history", ""),
    )
    print(f"Question for Tavily: {question_for_tavily}")

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    # Perform the search using Tavily
    response = tavily_client.search(question_for_tavily,search_depth="advanced", include_answer="advanced")

    # Use the response from Tavily to get the final answer
    Tavily_answer = response['answer']

    # Add Tavily_answer to the context
    if Tavily_answer:
        context = f"{context}\n\nHere is an LLM-generated answer based on an internet search. Take it into account along with the quotes and the Knesset member's background: {Tavily_answer}\n\n"

    else:
        # If Tavily_answer is empty, just use the original context
        context = f"{context}\n\n"

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

def clear_memory():
    memory.clear()

# Summarize conversation function
def summarize_conversation(conversation):
    summary_prompt = f"Summarize the following conversation in a concise manner:\n\n{conversation}\n\nSummary:"
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=summary_prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# if __name__ == "__main__":
#     # This is just for testing purposes, you can remove it when integrating into your app
#     user_input = "איך המדינה תראה אחרי המלחמה?"
#     kns_name = "Yair Lapid"
#     print(chatbot(user_input, kns_name))
#     clear_memory()