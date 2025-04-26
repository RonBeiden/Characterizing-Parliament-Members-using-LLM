import streamlit as st
from chat import *  # Importing the chatbot-related functions
from dotenv import load_dotenv
import pyodbc
load_dotenv()  # Load environment variables from .env file

def page_one():
    st.title("Choose a Knesset Member")
    
    # Image files (replace with actual paths)
    image_paths = [
        "KNS_members_images/Miri_Regev.jpg",
        "KNS_members_images/Yair_Lapid.jpg",
        "KNS_members_images/Itamar_Ben_Gvir.jpg",
        "KNS_members_images/Benjamin_Netanyahu.jpg",
        "KNS_members_images/Benny_Gantz.jpg"
    ]
    names = ["Miri Regev", "Yair Lapid", "Itamar Ben Gvir", "Benjamin Netanyahu", "Benny Gantz"]
    
    # Create equal columns based on the number of names
    cols = st.columns(len(names))
    
    # Add CSS for equal button sizes
    button_style = """
    <style>
    .stButton button {
        width: 100%;
        height: 80px;  /* Adjust the height as needed */
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    for i, col in enumerate(cols):
        with col:
            st.image(image_paths[i], width=100, caption=names[i], use_column_width=True)
            if st.button(f"{names[i]}"):
                st.session_state.selected_name = names[i]
                st.experimental_rerun()

def page_two():
    if st.session_state.selected_name[-1].isdigit():
        display_name = st.session_state.selected_name[:-3]
    else:
        display_name = st.session_state.selected_name

    st.title(f"Chat with {display_name}")
    # Select Knesset number (only once)
    if "knesset_number_selected" not in st.session_state:
        knesset_number = st.selectbox(
            "Select Knesset Number",
            options=get_knesset_numbers(display_name)
        )
        if st.button("Confirm Selection"):
            selected_number = "all" if knesset_number == "All" else str(knesset_number)
            if knesset_number == "All":
                st.session_state.selected_name = st.session_state.selected_name
            else:
                st.session_state.selected_name = f"{st.session_state.selected_name}_{selected_number}"
            st.session_state.knesset_number_selected = True  # Mark that Knesset number is chosen
            st.experimental_rerun()
        return  # Don't show chat yet until Knesset number selected

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

    if st.button("⬅️ Go Back"):
        memory.chat_memory.clear()
        keys_to_clear = ["selected_name", "knesset_number_selected", "messages", "conversation_count"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

def main():
    if 'selected_name' not in st.session_state:
        page_one()
    else:
        page_two()

if __name__ == "__main__":
    main()
