from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from collections import defaultdict

def extract_features(timetable):
    """Convert timetable into numerical features for Random Forest."""
    features = []
    labels = []

    for class_name, schedule in timetable.items():
        for day, periods in schedule.items():
            for period_index, subject in enumerate(periods):
                if subject:
                    teacher = subject.split("(")[-1].strip(")")
                    teacher_conflict = any(
                        timetable[c][day][period_index] == subject for c in timetable if c != class_name
                    )
                    consecutive_subject = (
                        period_index > 0 and timetable[class_name][day][period_index - 1] == subject
                    )

                    # Feature vector: [period_index, has_teacher_conflict, consecutive_subject]
                    features.append([period_index, int(teacher_conflict), int(consecutive_subject)])
                    labels.append(0 if teacher_conflict or consecutive_subject else 1)  # 0 = conflict, 1 = valid

    return np.array(features), np.array(labels)

def train_random_forest(features, labels):
    """Train a Random Forest classifier on timetable data."""
    if len(features) == 0:
        return None

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, clf.predict(X_test))
    print(f"Random Forest Accuracy: {accuracy * 100:.2f}%")

    return clf

def generate_timetable_with_accuracy(classes, lab_sessions):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods_per_day = 7

    
    timetable = {class_name: {day: [""] * periods_per_day for day in days} for class_name in classes.keys()}
    staff_schedule = defaultdict(lambda: {day: [False] * periods_per_day for day in days})

    
    for class_name, lab_details in lab_sessions.items():
        lab_days = set()
        alternate_flag = True
        for lab, mentors in lab_details.items():
            allocated = False
            for day in days:
                if allocated or day in lab_days:
                    continue

                if alternate_flag:
                    start_period = 0
                    slots = range(start_period, start_period + 4)
                else:
                    start_period = 4
                    slots = range(start_period, start_period + 3)

                if all(not staff_schedule[mentor][day][period] for mentor in mentors for period in slots):
                    for period in slots:
                        timetable[class_name][day][period] = f"{lab} (Lab: {', '.join(mentors)})"
                        for mentor in mentors:
                            staff_schedule[mentor][day][period] = True
                    lab_days.add(day)
                    allocated = True
                    alternate_flag = not alternate_flag
                    break

    
    for class_name, subjects in classes.items():
        for subject, details in subjects.items():
            repetitions = details['repetitions']
            staff_name = details['staff_name']
            allocated_periods = 0

            for day in days:
                if allocated_periods >= repetitions:
                    break
                for period in range(periods_per_day):
                    if allocated_periods >= repetitions:
                        break
                    if (not staff_schedule[staff_name][day][period]
                        and timetable[class_name][day][period] == ""
                        and (period == 0 or timetable[class_name][day][period - 1] != f"{subject} ({staff_name})")):
                        
                        timetable[class_name][day][period] = f"{subject} ({staff_name})"
                        staff_schedule[staff_name][day][period] = True
                        allocated_periods += 1

    for class_name, subjects in classes.items():
        subject_list = list(subjects.keys())
        subject_index = 0
        for day in days:
            for period in range(periods_per_day):
                if timetable[class_name][day][period] == "":
                    subject = subject_list[subject_index % len(subject_list)]
                    staff_name = subjects[subject]['staff_name']
                    if (not staff_schedule[staff_name][day][period]
                        and (period == 0 or timetable[class_name][day][period - 1] != f"{subject} ({staff_name})")):
                        
                        timetable[class_name][day][period] = f"{subject} ({staff_name})"
                        staff_schedule[staff_name][day][period] = True
                    subject_index += 1

    
    features, labels = extract_features(timetable)

    
    clf = train_random_forest(features, labels)

    
    if clf:
        predictions = clf.predict(features)
        valid_percentage = (np.sum(predictions) / len(predictions)) * 100
        print(f"Timetable Validity (Predicted by Random Forest): {valid_percentage:.2f}%")

    return timetable


classes = {
    "Class A": {
        "Math": {"repetitions": 3, "staff_name": "Teacher 1"},
        "Science": {"repetitions": 3, "staff_name": "Teacher 2"}
    }
}

lab_sessions = {
    "Class A": {
        "Physics Lab": ["Teacher 3"],
        "Chemistry Lab": ["Teacher 4"]
    }
}

timetable = generate_timetable_with_accuracy(classes, lab_sessions)
