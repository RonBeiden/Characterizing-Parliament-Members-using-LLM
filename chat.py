from setup import *
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

additional_info = """Miri Regev is a prominent and fiery figure in Israeli politics, known for her sharp rhetoric, decisive actions, and uncompromising style. As a former Minister of Transportation and Culture, as well as a long-serving Knesset member, Regev has solidified her reputation as a politician unafraid to spark controversy and boldly confront her critics.

Born in Kiryat Gat to a traditional Moroccan family, Regev embodies a story of social and cultural ascent. A former IDF spokesperson, she exudes deep Israeli patriotism and takes pride in championing her Mizrahi roots. She fiercely advocates for values of Zionism, national pride, and traditional identity, while strongly opposing any expression of anti-Israeli sentiment or internal criticism of the state.

With her forceful and direct style, Regev never hesitates to voice her opinions, even when they provoke heated debates. She is perceived as a defender of Israel’s “authentic” cultural heritage, promoting social issues focused on marginalized populations and striving to ensure that her agenda reflects a strong and proud Israeli identity."""

# Define the prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "human_input", "context", "kns_name","additional_info"],
    template="""You are {kns_name}, a member of the Israeli Knesset. 
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
system_message="""
You act as a member of the Knesset in the State of Israel who holds a dialogue with a citizen.  
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
"""

def chatbot(user_input):
    context = RAG(KNS_member=KNS_collection, query=user_input)
    
    # Explicitly pass ALL required variables
    response = conversation.run(
        human_input=user_input,
        context=context,
        kns_name=kns_name,
        additional_info=additional_info,
        chat_history=memory.load_memory_variables({}).get("chat_history", ""),
        system_message=system_message
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
