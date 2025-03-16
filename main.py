# from chat import *

# def main():
#     st.title("The Knesset Chatbot")

#     # Initialize session state
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []
#     if 'conversation_count' not in st.session_state:
#         st.session_state.conversation_count = 0

#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Chat input
#     if prompt := st.chat_input("What is your question?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Get chatbot response
#         response = chatbot(prompt)

#         # Display assistant response
#         with st.chat_message("assistant"):
#             st.markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})

#         # Increment conversation count
#         st.session_state.conversation_count += 1

#         # If 10 user messages have been processed, summarize and update memory
#         if st.session_state.conversation_count % 10 == 0:
#             conversation = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-20:]])
#             summary = summarize_conversation(conversation)
#             memory.chat_memory.add_user_message("Previous conversation summary")
#             memory.chat_memory.add_ai_message(summary)
#             st.session_state.messages = [{"role": "system", "content": f"Conversation summary: {summary}"}]

# if __name__ == "__main__":
#     main()
import streamlit as st
from chat import *  # Importing the chatbot-related functions

def page_one():
    st.title("Choose a Knesset Member")
    
    # Image files (replace with actual paths)
    image_paths = [
        "KNS_members_images/Miri_Regev.jpg",
        "KNS_members_images/Yair_Lapid.jpg",
        "KNS_members_images/Itamar_Ben_Gvir.jpg"
    ]
    names = ["Miri Regev", "Yair Lapid", "Itamar Ben Gvir"]
    
    cols = st.columns(len(names))
    for i, col in enumerate(cols):
        with col:
            st.image(image_paths[i], width=100, caption=names[i], use_column_width=True)
            if st.button(f"Chat with {names[i]}"):
                st.session_state.selected_name = names[i]
                st.experimental_rerun()

# Page 2 - Chatbot page
def page_two():
    st.title(f"Chatbot with {st.session_state.selected_name}")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = chatbot(prompt, st.session_state.selected_name)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.conversation_count += 1
        if st.session_state.conversation_count % 10 == 0:
            conversation = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-20:]])
            summary = summarize_conversation(conversation)
            memory.chat_memory.add_user_message("Previous conversation summary")
            memory.chat_memory.add_ai_message(summary)
            st.session_state.messages = [{"role": "system", "content": f"Conversation summary: {summary}"}]

def main():
    if 'selected_name' not in st.session_state:
        page_one()
    else:
        page_two()

if __name__ == "__main__":
    main()