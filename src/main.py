import streamlit as st
from chat import *  # Importing the chatbot-related functions
load_dotenv()  # Load environment variables from .env file

def page_one():
    st.title("Choose a Knesset Member")
    
    # Image files (replace with actual paths)
    image_paths = [
        "../KNS_members_images/Miri_Regev.jpg",
        "../KNS_members_images/Yair_Lapid.jpg",
        "../KNS_members_images/Itamar_Ben_Gvir.jpg",
        "../KNS_members_images/Benjamin_Netanyahu.jpg",
        "../KNS_members_images/Benny_Gantz.jpg"
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


# Page 2 - Chatbot page
def page_two():
    st.title(f"Chatbot with {st.session_state.selected_name}")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
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

    # "Go Back" button that clears session state and restarts session
    if st.button("⬅️ Go Back"):
        # Reset chat history and selected member explicitly
        keys_to_clear = ["selected_name", "messages", "conversation_count"]
        memory.chat_memory.clear()
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]  # Remove specific keys

        st.experimental_rerun()  # Ensure the UI updates

def main():
    if 'selected_name' not in st.session_state:
        page_one()
    else:
        page_two()

if __name__ == "__main__":
    main()
