import json
from collections import OrderedDict
from reader import open_excel
from models import Course, CourseRaw, Student, StudentRaw, Requirement, timestamp_after


def dump_data():
    years = [2013, 2014, 2015, 2016]

    def students_ext(year): return 'data/alumnos{}.xlsx'.format(year)

    def courses_ext(year): return 'data/cursos{}.xlsx'.format(year)

    students_files = {year: students_ext(year) for year in years}

    courses_files = {year: courses_ext(year) for year in years}

    students_data = {}
    courses_data = {}

    for year in years:
        students_data[year] = open_excel(
            students_files[year]).to_dict(orient='records')
        courses_data[year] = open_excel(
            courses_files[year]).to_dict(orient='records')

    for year in years:
        for student_datum in students_data[year]:
            StudentRaw(**student_datum)

        for course_datum in courses_data[year]:
            CourseRaw(**course_datum)

    with open('processed_data/student_objects.json', 'w', encoding='utf8') as student_objects_file:
        data = [s.__dict__ for s in StudentRaw.all]
        json.dump(data, student_objects_file)

    with open('processed_data/course_objects.json', 'w', encoding='utf8') as course_objects_file:
        data = [c.__dict__ for c in CourseRaw.all]
        json.dump(data, course_objects_file)

    with open('processed_data/student_dict.json', 'w', encoding='utf8') as student_dict_file:
        data = StudentRaw.prop_names
        json.dump(data, student_dict_file)

    with open('processed_data/course_dict.json', 'w', encoding='utf8') as course_dict_file:
        data = CourseRaw.prop_names
        json.dump(data, course_dict_file)

    with open('processed_data/student_field_possibilities.json', 'w', encoding='utf8') as student_field_possibilities_file:
        data = StudentRaw.prop_names
        field_hash = {
            v: list(set([getattr(s, v) for s in StudentRaw.all])) for v in data.values()}
        json.dump(field_hash, student_field_possibilities_file)

    with open('processed_data/course_field_possibilities.json', 'w', encoding='utf8') as course_field_possibilities_file:
        data = CourseRaw.prop_names
        field_hash = {
            v: list(set([getattr(s, v) for s in CourseRaw.all])) for v in data.values()}
        json.dump(field_hash, course_field_possibilities_file)


def load_objects():
    with open('processed_data/student_objects.json', 'r', encoding='utf-8') as student_objects_file:
        data = json.load(student_objects_file)
        [Student(datum) for datum in data]
    with open('processed_data/course_objects.json', 'r', encoding='utf-8') as course_objects_file:
        data = json.load(course_objects_file)
        [Course(datum) for datum in data]


def load_requirements():
    with open('data/requirements.json', 'r', encoding='utf-8') as requirements_file:
        data = json.load(requirements_file)
        [Requirement(**datum) for datum in data]


if __name__ == '__main__':
        # dump_data()
    load_requirements()
    load_objects()

    potential_requirements = []
    for course in Requirement.all.values():
        potential_requirements += course.valid_initials

    Student.all = Student.filter_by('admission_way', 'ORDINARIA PAA')
    Student.all = Student.filter_by('admission_year', '2013')
    Student.all = Student.filter_by('curriculum', 'C2013')
    Student.all = Student.filter_by('admission_type', '-')

    valid_students = list(Student.all.keys())
    Course.all = Course.from_students(valid_students)
    Course.all = Course.with_initials(potential_requirements)

    for course in Course.all.values():
        Student.all[course.student_id].courses[course.initials].append(course)
        Student.all[course.student_id].semesters[course.relative_semester()].append(
            course)

    semester_timestamps = {
        1: {
            "start_date": "03/05",
            "end_date": "07/04",
        },
        2: {
            "start_date": "08/04",
            "end_date": "12/15",
        },
        3: {
            "start_date": "01/04",
            "end_date": "02/22",
        }
    }

    # 1º, 2º and TAV for 5 years (from 2013 to the end of 2017)
    logs = ["Case ID,Start Timestamp,End Timestamp,Activity\n"]

    progress = Student.all['3612013'].progress_per_semester()
    for i in progress.values():
        print(i)

    for student_id, student in Student.all.items():
        progresses = student.progress_per_semester()
        initial_log = "{},{},{},{}\n".format(
            student.student_number, "2013/03/01", "2013/03/02", "Start university career")
        print(initial_log)
        logs.append(initial_log)
        last_progress = None
        for semester_number, data in progresses.items():
            activity = data['activity']
            if activity == None:
                continue
            last_progress = data
            activity_log = "{},{},{},{}\n".format(
                student.student_number, data['start_timestamp'], data['end_timestamp'], activity)

            tav_semester = False    
            semester_activity = "End of semester {}".format(
                semester_number - int(semester_number / 3))
            if semester_number % 3 == 0:
                semester_activity = "End of TAV semester {}".format(
                    int(semester_number / 3))
                tav_semester = True
            semester_start = data['semester_start']
            semester_end = data['semester_end']
            semester_log = "{},{},{},{}\n".format(
                student.student_number, semester_start, semester_end, semester_activity)
            if tav_semester and data['taken'] == 0:
                continue
            print(semester_log)
            logs.append(semester_log)
            print(activity_log)
            logs.append(activity_log)
        if (not student.requirements_ready) and last_progress:
            start_date = timestamp_after(last_progress['start_timestamp'], 2)
            end_date = timestamp_after(last_progress['end_timestamp'], 2)
            accumulated = last_progress['accumulated']
            percentage = last_progress['percentage']
            unqualified_activity = "Not qualified. < 100%"
            incomplete_requirements_log = "{},{},{},{}\n".format(
                student.student_number, start_date, end_date, unqualified_activity)
            logs.append(incomplete_requirements_log)
            print(incomplete_requirements_log)
        final_log = "{},{},{},{}\n".format(
            student.student_number, "2018/05/01", "2018/05/02", "Today")
        print(final_log)
        logs.append(final_log)

    with open('processed_data/logs.csv', 'w', encoding='utf-8') as log_file:
        for log in logs:
            log_file.write(log)
