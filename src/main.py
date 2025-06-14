import streamlit as st
from chat import *  # Importing the chatbot-related functions
from dotenv import load_dotenv
import pyodbc
import os

load_dotenv()  # Load environment variables from .env file

def page_one():
    st.markdown("""
        <h1 style='text-align: center; font-size: 3rem; margin-bottom: 2rem; color: white;'>
            🗳️ Choose a Knesset Member
        </h1>
    """, unsafe_allow_html=True)

    folder_name = 'KNS_members_images'
    image_paths, names = [], []

    for filename in os.listdir(folder_name):
        if filename.endswith('.jpg'):
            image_paths.append(f'{folder_name}/{filename}')
            name = os.path.splitext(filename)[0].replace('_', ' ')
            names.append(name)

    cols_per_row = 5

    # --- Restored original button style ---
    st.markdown("""
    <style>
        .stButton button {
            width: 100%;
            height: 80px;
        }
    </style>
    """, unsafe_allow_html=True)

    for i in range(0, len(names), cols_per_row):
        row_images = image_paths[i:i+cols_per_row]
        row_names = names[i:i+cols_per_row]
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            if j < len(row_images):
                with col:
                    st.image(row_images[j], width=120, caption=row_names[j])
                    if st.button(row_names[j], key=f"btn_{i+j}"):
                        st.session_state.selected_name = row_names[j]
                        st.experimental_rerun()



def page_two():
    if st.session_state.selected_name[-1].isdigit():
        display_name = st.session_state.selected_name[:-3]
    else:
        display_name = st.session_state.selected_name

    st.markdown(f"""
        <h1 style='text-align: center; font-size: 3rem; margin-bottom: 2rem; color: white;'>
            💬 Chat with {display_name}
        </h1>""", unsafe_allow_html=True)

    kns_nums = get_knesset_numbers(display_name)
    kns_nums.insert(0, "All")
    if "knesset_number_selected" not in st.session_state:
        knesset_number = st.selectbox("🗂️ Select Knesset Number", options=kns_nums)
        if st.button("✅ Confirm Selection"):
            selected_number = "all" if knesset_number == "All" else str(knesset_number)
            st.session_state.selected_name = f"{display_name}_{selected_number}" if knesset_number != "All" else display_name
            st.session_state.knesset_number_selected = True
            st.experimental_rerun()
        return

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("💡 What would you like to ask?"):
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

    if st.button("⬅️ Go Back to Selection"):
        memory.chat_memory.clear()
        for key in ["selected_name", "knesset_number_selected", "messages", "conversation_count"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()


def main():
    if 'selected_name' not in st.session_state:
        page_one()
    else:
        page_two()

if __name__ == "__main__":
    main()
