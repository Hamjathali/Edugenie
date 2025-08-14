import streamlit as st
import google.generativeai as genai
import time

# Set your Gemini API key directly (for development/testing ONLY - not for production!)
GEMINI_API_KEY = "AIzaSyBIGp9LtXnHpYFoUpAWg05mpO8aW6G_e0Q"  # Replace with your actual API key

if not GEMINI_API_KEY:
    st.error("Gemini API key not set. Please set GEMINI_API_KEY directly in the code.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


# Path to the college information text file
COLLEGE_INFO_FILE = "testfile.txt"

def load_college_info(filepath):
    """Loads college information from a text file."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "College information file not found."
    except Exception as e:
        return f"Error loading college information: {e}"

def chatbot_response(user_input):
    """Generates a response using Gemini, incorporating college info from file."""

    college_info = load_college_info(COLLEGE_INFO_FILE)

    if college_info:
        prompt = f"""
        You are a college chatbot. Answer questions about the college based on the following information:

        {college_info[:4000]} # Limit college info to avoid token limits
        Note: if you dont know about any information that the person ask please replay as a chatbot i am limited to certain info only will update soon dont replay except this

        User: {user_input}
        Chatbot:
        """

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating a response: {e}"
    else:
        return "Sorry, I couldn't retrieve college information."

# Streamlit App
st.title("College Chatbot")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    clear_chat = st.button("Clear Chat History")
    if clear_chat:
        st.session_state.messages = []

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about the college..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simulate typing delay
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = chatbot_response(prompt)
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05) # Adjust delay as needed
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display college info file content in an expander
st.expander("College Information").write(load_college_info(COLLEGE_INFO_FILE))

# Add a status message while waiting for the AI response.
if "messages" in st.session_state and len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    with st.status("Thinking..."):
        time.sleep(1) # Simulate the time spent processing.