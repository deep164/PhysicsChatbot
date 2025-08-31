# filename: physics_chatbot.py

import streamlit as st
from openai import OpenAI

# -------------------------
# Streamlit App Title
# -------------------------
st.set_page_config(page_title="Physics Chatbot", page_icon="⚛️")
st.title("⚛️ Physics Chatbot")
st.subheader("Ask me any physics concept and I will explain it!")

# -------------------------
# Initialize OpenAI client
# -------------------------
api_key = st.secrets["OPENAI_API_KEY"]  # Streamlit ke liye recommended
client = OpenAI(api_key=api_key)

# -------------------------
# Session State for Chat History
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# User Input
# -------------------------
user_input = st.text_input("Type your question here:")

def get_response(user_input):
    """Function to get GPT response"""
    messages = [{"role": "system", "content": "You are a physics tutor. Explain concepts clearly with examples."}]
    
    # Add chat history
    for chat in st.session_state.history:
        messages.append({"role": "user", "content": chat["user"]})
        messages.append({"role": "assistant", "content": chat["bot"]})
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    
    answer = response.choices[0].message.content
    return answer

# -------------------------
# Display Chat
# -------------------------
if st.button("Send") and user_input:
    bot_response = get_response(user_input)
    
    # Store in session
    st.session_state.history.append({"user": user_input, "bot": bot_response})
    
    # Clear input
    user_input = ""
    
# Display all chats
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**PhysicsBot:** {chat['bot']}")
    st.markdown("---")

# -------------------------
# Reset Chat
# -------------------------
if st.button("Reset Chat"):
    st.session_state.history = []
    st.experimental_rerun()
