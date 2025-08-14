import streamlit as st
from model import generate_timetable_with_accuracy
import pandas as pd

st.set_page_config(page_title="Smart Timetable Generator", layout="wide")

st.title("📅 Smart Timetable Generator with ML Accuracy")

# UI for number of classes
num_classes = st.number_input("Enter number of classes", min_value=1, max_value=10, step=1)

classes = {}
lab_sessions = {}

st.markdown("---")
st.header("📝 Enter Class Details")

for i in range(num_classes):
    st.subheader(f"Class {i+1}")
    class_name = st.text_input(f"Enter name for Class {i+1}", key=f"class_name_{i}")
    if class_name == "":
        continue

    num_subjects = st.number_input(f"Number of subjects for {class_name}", min_value=1, max_value=10, key=f"num_subjects_{i}")
    classes[class_name] = {}

    for j in range(num_subjects):
        col1, col2, col3 = st.columns(3)
        with col1:
            subject_name = st.text_input(f"Subject {j+1} name", key=f"subject_name_{i}_{j}")
        with col2:
            repetitions = st.number_input(f"Repetitions for {subject_name}", min_value=1, max_value=10, key=f"repetitions_{i}_{j}")
        with col3:
            staff_name = st.text_input(f"Staff for {subject_name}", key=f"staff_name_{i}_{j}")
        if subject_name:
            classes[class_name][subject_name] = {
                'repetitions': repetitions,
                'staff_name': staff_name
            }

    st.markdown(f"🔬 Lab Sessions for {class_name}")
    num_labs = st.number_input(f"Number of labs for {class_name}", min_value=0, max_value=5, key=f"num_labs_{i}")
    lab_sessions[class_name] = {}

    for k in range(num_labs):
        col1, col2 = st.columns(2)
        with col1:
            lab_name = st.text_input(f"Lab {k+1} name", key=f"lab_name_{i}_{k}")
        with col2:
            mentors = st.text_input(f"Mentors (comma-separated)", key=f"mentors_{i}_{k}")
        if lab_name and mentors:
            mentor_list = [m.strip() for m in mentors.split(',')]
            lab_sessions[class_name][lab_name] = mentor_list

st.markdown("---")

if st.button("🚀 Generate Timetable"):
    with st.spinner("Generating timetable and evaluating..."):
        timetable = generate_timetable_with_accuracy(classes, lab_sessions)

        st.success("✅ Timetable generated!")

        st.markdown("### 🗓️ Final Timetable")

        for class_name, schedule in timetable.items():
            st.subheader(f"📘 {class_name}")
            df = pd.DataFrame(schedule).T
            df.columns = [f"Period {i+1}" for i in range(df.shape[1])]
            st.dataframe(df, use_container_width=True)
