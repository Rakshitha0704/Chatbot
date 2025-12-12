import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Streamlit page settings
st.set_page_config(
    page_title="Chat with Prep-Pro",
    page_icon="🤖",
    layout="centered"
)

# Load your Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Supported model (latest)
MODEL_NAME = "llama-3.3-70b-versatile"

# Initialize chat history if not present
if "history" not in st.session_state:
    st.session_state.history = []

# App title
st.title("🤖 Prep-Pro ChatBot")

# Display previous messages
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Ask anything...")

if user_prompt:
    # Add user message to history
    st.session_state.history.append({
        "role": "user",
        "content": user_prompt
    })

    st.chat_message("user").markdown(user_prompt)

    try:
        # Send request to Groq API
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.history
            ],
            temperature=0.7,
        )

        # Correct way to extract response content
        reply = response.choices[0].message.content

        # Save assistant reply to history
        st.session_state.history.append({
            "role": "assistant",
            "content": reply
        })

        # Display assistant message
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"Error: {e}")
