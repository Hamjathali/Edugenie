from flask import Flask, render_template, request
from model import generate_timetable_with_accuracy

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generate():
    num_classes = int(request.form['num_classes'])
    classes = {}
    lab_sessions = {}

    for i in range(num_classes):
        class_name = request.form[f'class_name_{i}']
        num_subjects = int(request.form[f'num_subjects_{i}'])
        classes[class_name] = {}

        for j in range(num_subjects):
            subject_name = request.form[f'subject_name_{i}_{j}']
            repetitions = int(request.form[f'repetitions_{i}_{j}'])
            staff_name = request.form[f'staff_name_{i}_{j}']
            classes[class_name][subject_name] = {
                'repetitions': repetitions,
                'staff_name': staff_name
            }

        num_labs = int(request.form[f'num_labs_{i}'])
        lab_sessions[class_name] = {}
        for k in range(num_labs):
            lab_name = request.form[f'lab_name_{i}_{k}']
            mentors = request.form[f'mentors_{i}_{k}'].split(',')
            lab_sessions[class_name][lab_name] = mentors

    timetable = generate_timetable_with_accuracy(classes, lab_sessions)
    return render_template('timetable.html', timetable=timetable)
if __name__ == '__main__':
    app.run(debug=True)