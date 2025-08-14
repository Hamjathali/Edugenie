# 📚 EduGenie - College AI Toolkit

Welcome to **EduGenie**, an all-in-one AI-powered toolkit specially built for college automation! 🎓🚀  
This project brings together the power of **AI, Streamlit, and Python** to make faculty tasks easier, smarter, and faster.

---

## 🛠 Features

✅ **Secure Login System**  
✅ **Logout Button** to safely end sessions  
✅ **Feedback Collection** with ratings and charts  
✅ **Beautiful, user-friendly interface**

---

## 💡 How to Run This Project

Make sure you have Python installed (version 3.11 or higher).

To run the project:

```bash
streamlit run main.py
```

This will start the Streamlit web app in your browser.

---

## 🔥 Tools Inside

### 1. 📅 Automated Timetable Generator (Main Highlight ✨)

- Automatically generates complete department-wise **theory and lab timetables**.
- Smart allocation based on:
  - Staff availability
  - Avoiding staff conflicts
  - Preventing back-to-back same subject periods
- Uses **Random Forest Algorithm** to validate and measure **timetable quality**.
- Ensures fairness and optimal distribution of sessions across the week.
- Originally built for **IFET College**, but easily adaptable to other institutions.

---

### 2. 📝 AI-based Question Paper Generator

- Upload your question bank in **PDF or Word format**.
- AI (Gemini API) generates random questions categorized by difficulty:
  - **Easy**, **Medium**, **Hard**
- Instantly download the formatted paper in **PDF and DOCX**.

---

### 3. 🤖 College Information Chatbot

- Ask any question about the college: 🎓
  - Departments
  - Events
  - Admission process
  - Contact info
- Powered by **Gemini AI API** for intelligent and fast responses.

---

## 🔐 Login and Logout System

- Access is restricted to authorized users via a **secure login system**.
- A **logout button** is placed on the interface for session control.

---

## 🗣️ Feedback Collection

- Allows users to rate and give feedback about the tool.
- Ratings are displayed as a **bar chart**.
- Feedbacks are saved in a file (`feedbacks.txt`) for further analysis.

---

## 🗺️ Extras

- Shows IFET College’s location on an embedded map.
- Includes developer credits at the bottom.

---

## ⚙ Tech Stack

- **Python 3.11+**
- **Streamlit** (main interface)
- **Flask** (backend support for timetable generator)
- **Gemini AI API** (chatbot + question generator)
- **Pandas**
- **HTML/CSS** (used in Flask templates)

---

## 🏁 Future Enhancements

- Timetable conflict resolution UI
- Auto-emailing of question papers to staff
- Student portal integration
