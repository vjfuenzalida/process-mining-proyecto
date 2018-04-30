import json
from reader import open_excel
from models import CourseInstance, CourseInstanceRaw, Student, StudentRaw

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
            CourseInstanceRaw(**course_datum)

    with open('processed_data/student_objects.json', 'w', encoding='utf8') as student_objects_file:
        data = [s.__dict__ for s in StudentRaw.all]
        json.dump(data, student_objects_file)

    with open('processed_data/course_objects.json', 'w', encoding='utf8') as course_objects_file:
        data = [c.__dict__ for c in CourseInstanceRaw.all]
        json.dump(data, course_objects_file)

    with open('processed_data/student_dict.json', 'w', encoding='utf8') as student_dict_file:
        data = StudentRaw.prop_names
        json.dump(data, student_dict_file)

    with open('processed_data/course_dict.json', 'w', encoding='utf8') as course_dict_file:
        data = CourseInstanceRaw.prop_names
        json.dump(data, course_dict_file)

    with open('processed_data/student_field_possibilities.json', 'w', encoding='utf8') as student_field_possibilities_file:
        data = StudentRaw.prop_names
        field_hash = {v: list(set([getattr(s, v) for s in StudentRaw.all])) for v in data.values()}
        json.dump(field_hash, student_field_possibilities_file)

    with open('processed_data/course_field_possibilities.json', 'w', encoding='utf8') as course_field_possibilities_file:
        data = CourseInstanceRaw.prop_names
        field_hash = {v: list(set([getattr(s, v) for s in CourseInstanceRaw.all])) for v in data.values()}
        json.dump(field_hash, course_field_possibilities_file)

def load_objects():
    with open('processed_data/student_objects.json', 'r', encoding='utf-8') as student_objects_file:
        data = json.load(student_objects_file)
        objects = [Student(datum) for datum in data]
        Student.all = objects
    with open('processed_data/course_objects.json', 'r', encoding='utf-8') as course_objects_file:
        data = json.load(course_objects_file)
        objects = [CourseInstance(datum) for datum in data]
        CourseInstance.all = objects


if __name__ == '__main__':
    # dump_data()
    load_objects()
    print(Student.filter_by('admission_way', 'ORDINARIA PAA'))
    # print(CourseInstance.filter_by('initials', 'ING1004'))