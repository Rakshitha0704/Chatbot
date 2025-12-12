import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load the environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Prep-pro!",
    page_icon=":brain:",
    layout="centered",
)

# Get the API key from environment
GOOGLE_API_KEY = os.getenv("API-KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.0-flash')  # Adjust based on library version

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 Prep Pro - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Prep-Pro...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    try:
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Assuming gemini_response has a `.text` field, if not adjust accordingly
        response_text = gemini_response.text if hasattr(gemini_response, 'text') else "Sorry, no response received."
        
        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(response_text)

    except Exception as e:
        st.error(f"Error: {e}")
