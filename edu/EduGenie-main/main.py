import streamlit as st
import os

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

   
import streamlit as st
import subprocess
import webbrowser
import os


st.set_page_config(page_title="EduGenie", layout="wide")


with st.sidebar:
    st.markdown("<h1 style='text-align: left; font-size:36px;'>EduGenie</h1>", unsafe_allow_html=True)
    st.image("edu/EduGenie-main/assets/logo.png", width=150)
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
    from datetime import datetime
    st.caption(f"🕒 Accessed on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    
    logout_col = st.columns([1, 1, 1])[1]  
    with logout_col:
        if st.button("🔒 Logout", key="logout", help="Click to logout", use_container_width=True):
            st.session_state.logged_in = False
            st.experimental_rerun()
    


    


st.markdown("<h1 style='text-align: center;'> College AI Toolkit</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Select a tool to get started</p>", unsafe_allow_html=True)
st.markdown("---")

# Three column layout for tools
col1, col2, col3 = st.columns(3)

with col1:
    st.image("edu/EduGenie-main/assets/question_paper.jpg", use_container_width=True)

    if st.button("📝 Generate Question Paper"):
        subprocess.Popen(["streamlit", "run", "question_paper_app.py"])
        st.success("Launching Question Paper Generator...")
    st.markdown("""
    <div style='padding: 10px; background-color: #1e1e1e; border-radius: 10px; color: #cccccc; margin-top: 10px;'>
        <h4>📝 What does the Question Paper Generator do?</h4>
        <p>
            This intelligent tool allows faculty to upload a question bank in <b>PDF or Word format</b>.
            Using the <b>Gemini AI API</b>, it auto-generates exam-ready questions categorized by difficulty: <b>Easy, Medium, Hard</b>.
        </p>
        <p>
            Users can also <b>manually input custom questions</b> for greater flexibility.
            The output is a neatly formatted question paper in both <b>PDF and Word</b> formats – ready to print!
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    image_path_chatbot = os.path.join(os.path.dirname(__file__), "assets", "chatbot.jpg")
    st.image(image_path_chatbot, use_container_width=True)

    if st.button("💬 Open College Chatbot"):
        subprocess.Popen(["streamlit", "run", "college_chatbot.py"])
        st.success("Launching College Chatbot...")
        
    st.markdown("""
    <div style='padding: 10px; background-color: #1e1e1e; border-radius: 10px; color: #cccccc; margin-top: 10px;'>
        <h4>🤖 What does the College Chatbot do?</h4>
        <p>
            Our AI-powered chatbot provides instant answers to common college-related queries, such as:
            admission details, departments, events, contact info, and more. 
            Built using the <b>Gemini AI API</b>, this assistant understands natural language and responds in real time.
        </p>
        <p>
            It's your 24/7 digital guide for everything about our college!
        </p>
    </div>
    """, unsafe_allow_html=True)


with col3:
    image_path_timetable = os.path.join(os.path.dirname(__file__), "assets", "chatbot.jpg")
    st.image(image_path_timetable, use_container_width=True)

    if st.button("📅 Generate Timetable"):
        subprocess.Popen(["streamlit", "run", "timetable_app.py"])
        st.success("Launching Timetable Generator...")
    st.markdown("""
    <div style='padding: 10px; background-color: #1e1e1e; border-radius: 10px; color: #cccccc; margin-top: 10px;'>
        <h4>📅 What does the Timetable Generator do?</h4>
        <p>
            A fully automated timetable generation system tailored for <b>IFET College</b>. 
            It efficiently generates department-wide schedules for both <b>theory and lab classes</b>, 
            considering staff availability and department-wise constraints.
        </p>
        <p>
            The system supports <b>custom lab session allocation</b> and prevents scheduling conflicts – 
            offering a smart solution to an otherwise time-consuming manual process.
        </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")
st.markdown("<p style='text-align: center;'>💡 Developed for the event at IFET College Of Engineering  of Event name Ibaklava </p>", unsafe_allow_html=True)




st.markdown("---")
st.header("🗣️ We Value Your Feedback")
st.write("Please let us know your thoughts about the College AI Toolkit!")

with st.form("feedback_form"):
    name = st.text_input("Your Name")
    feedback = st.text_area("Your Feedback", placeholder="Share your thoughts, suggestions, or issues you faced...")
    rating = st.slider("Rate this App", 1, 5, 3)

    submitted = st.form_submit_button("Submit Feedback")
    if submitted:
        
        with open("feedbacks.txt", "a") as f:
            f.write(f"Name: {name}\nRating: {rating}/5\nFeedback: {feedback}\n{'-'*40}\n")
        st.success("✅ Thank you for your valuable feedback!")




import pandas as pd
import altair as alt

ratings = []
with open(feedback.txt, "r") as f:
    feedbacks = f.readlines()
    for line in f:
        if "Rating" in line:
            ratings.append(int(line.split(":")[1].split("/")[0].strip()))

if ratings:
    df = pd.DataFrame(ratings, columns=["Rating"])
    rating_counts = df["Rating"].value_counts().sort_index().reset_index()
    rating_counts.columns = ["Rating", "Count"]

    
    chart = alt.Chart(rating_counts).mark_bar().encode(
        x=alt.X("Rating:O", title="Rating"),
        y=alt.Y("Count:Q", title="Count"),
        color=alt.Color("Rating:O", scale=alt.Scale(domain=[1, 2, 3, 4, 5], range=["red", "orange", "yellow", "green", "blue"])),
        tooltip=["Rating", "Count"]
    ).properties(
        title="Feedback Ratings Distribution"
    )

    st.altair_chart(chart, use_container_width=True)



import pandas as pd
st.map(pd.DataFrame({'lat': [11.9207389], 'lon': [79.6107319]}))  # IFET College coords


with st.expander("📢 About This App / Credits"):
    st.markdown("""
    **Developed by:** Team Code Shelby:Basheer Ahamed A, Hamjathali I
    **Tech Stack:** Streamlit, Gemini AI, Python, Flask  
    **Purpose:** Smart automation tools for college use  
    """)