import streamlit as st
import os
import subprocess
from datetime import datetime
import pandas as pd
import altair as alt

# -------------------- LOGIN SYSTEM --------------------
USER_CREDENTIALS = {
    "admin": "admin123",
    "user1": "pass1",
    "sathish": "cse123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to EduGenie")
    st.subheader("Please enter your credentials to continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

# -------------------- APP LAYOUT --------------------
st.set_page_config(page_title="EduGenie", layout="wide")

with st.sidebar:
    st.markdown("<h1 style='text-align: left; font-size:36px;'>EduGenie</h1>", unsafe_allow_html=True)
    st.image(os.path.join("assets", "logo.png"), width=150)
    st.title("AI Tools Suite")
    st.markdown("""
    👋 Welcome to our **AI-powered college tools** !

    Features:
    - 📄 Question Paper Generator  
    - 🤖 College Info Chatbot  
    - 🗓️ Timetable Generator

    Built using **Python, Streamlit, Gemini AI API and other Libraries**
    """)
    st.info("Created by: Basheer Ahamed A, Hamjathali I")
    st.caption(f"🕒 Accessed on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")

    logout_col = st.columns([1, 1, 1])[1]
    with logout_col:
        if st.button("🔒 Logout", key="logout", help="Click to logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

st.markdown("<h1 style='text-align: center;'> College AI Toolkit</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Select a tool to get started</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- TOOL CARDS --------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.image(os.path.join("assets", "question_paper.jpg"), use_container_width=True)
    if st.button("📝 Generate Question Paper"):
        subprocess.Popen(["streamlit", "run", "question_paper_app.py"])
        st.success("Launching Question Paper Generator...")

with col2:
    st.image(os.path.join("assets", "chatbot.jpg"), use_container_width=True)
    if st.button("💬 Open College Chatbot"):
        subprocess.Popen(["streamlit", "run", "college_chatbot.py"])
        st.success("Launching College Chatbot...")

with col3:
    st.image(os.path.join("assets", "timetable.jpg"), use_container_width=True)
    if st.button("📅 Generate Timetable"):
        subprocess.Popen(["streamlit", "run", "timetable_app.py"])
        st.success("Launching Timetable Generator...")

st.markdown("---")
st.markdown("<p style='text-align: center;'>💡 Developed for the event at IFET College Of Engineering - Event: Ibaklava </p>", unsafe_allow_html=True)

# -------------------- FEEDBACK FORM --------------------
st.markdown("---")
st.header("🗣️ We Value Your Feedback")
st.write("Please let us know your thoughts about the College AI Toolkit!")

feedback_file = "feedbacks.txt"
if not os.path.exists(feedback_file):
    open(feedback_file, "w").close()

with st.form("feedback_form"):
    name = st.text_input("Your Name")
    feedback = st.text_area("Your Feedback", placeholder="Share your thoughts, suggestions, or issues you faced...")
    rating = st.slider("Rate this App", 1, 5, 3)

    submitted = st.form_submit_button("Submit Feedback")
    if submitted:
        with open(feedback_file, "a") as f:
            f.write(f"Name: {name}\nRating: {rating}/5\nFeedback: {feedback}\n{'-'*40}\n")
        st.success("✅ Thank you for your valuable feedback!")

# -------------------- FEEDBACK CHART --------------------
ratings = []
with open(feedback_file, "r") as f:
    for line in f:
        if "Rating" in line:
            try:
                ratings.append(int(line.split(":")[1].split("/")[0].strip()))
            except:
                pass

if ratings:
    df = pd.DataFrame(ratings, columns=["Rating"])
    rating_counts = df["Rating"].value_counts().sort_index().reset_index()
    rating_counts.columns = ["Rating", "Count"]

    chart = alt.Chart(rating_counts).mark_bar().encode(
        x=alt.X("Rating:O", title="Rating"),
        y=alt.Y("Count:Q", title="Count"),
        color=alt.Color("Rating:O", scale=alt.Scale(domain=[1, 2, 3, 4, 5],
                                                   range=["red", "orange", "yellow", "green", "blue"])),
        tooltip=["Rating", "Count"]
    ).properties(title="Feedback Ratings Distribution")

    st.altair_chart(chart, use_container_width=True)

# -------------------- MAP --------------------
st.map(pd.DataFrame({'lat': [11.9207389], 'lon': [79.6107319]}))  # IFET College coords

# -------------------- CREDITS --------------------
with st.expander("📢 About This App / Credits"):
    st.markdown("""
    **Developed by:** Team Code Shelby: Basheer Ahamed A, Hamjathali I  
    **Tech Stack:** Streamlit, Gemini AI, Python, Flask  
    **Purpose:** Smart automation tools for college use  
    """)
