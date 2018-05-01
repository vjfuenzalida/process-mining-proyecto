from collections import defaultdict


def get_activity(taken, approved, accumulated):
    # LISTO
    percentage = accumulated * 100 / 16
    if accumulated == 16:
        if taken == 0:
            return None
        else:
            return "Qualified. 100% completed"
    # NO TOMÓ CURSOS
    elif taken == 0:
        return "No taken courses"
    # TOMÓ CURSOS
    elif taken > 0:
        if percentage <= 20:
            return "Approved. 1-20%"
        elif percentage <= 40:
            return "Approved. 21-40%"
        elif percentage <= 60:
            return "Approved. 41-60%"            
        elif percentage <= 80:
            return "Approved. 61-80%"
        elif percentage <= 99:
            return "Approved. 81-99%"                      


def timestamp_before(date, days):
    parsed = date.split("/")
    year = int(parsed[0])
    month = int(parsed[1])
    day = int(parsed[2])
    return "{:04d}/{:02d}/{:02d}".format(year, month, day - days)


def timestamp_after(date, days):
    parsed = date.split("/")
    year = int(parsed[0])
    month = int(parsed[1])
    day = int(parsed[2])
    return "{:04d}/{:02d}/{:02d}".format(year, month, day + days)


class Student:

    all = {}

    def __init__(self, data):
        self.__dict__ = data
        self.student_id = "{}{}".format(
            data['student_number'], data['admission_year'])
        Student.all.update({self.student_id: self})
        self.courses = defaultdict(list)
        self.semesters = defaultdict(list)
        self.semester_count = 3 * (2018 - int(data['admission_year']))
        self.requirements_ready = False
        self.requirements_ready_at = ""

    @classmethod
    def filter_by(cls, field, value):
        return {k: v for k, v in cls.all.items() if getattr(v, field) == value}

    def progress_per_semester(self):
        progresses = {}
        accumulated = 0
        for semester_number in range(1, self.semester_count + 1):
            semester = int(semester_number)
            start_timestamp, end_timestamp = Course.timestamp_from_relative(
                semester, self.admission_year)
            if semester in self.semesters.keys():
                courses = self.semesters[semester]
                taken = len(courses)
                approved = len([c for c in courses if float(
                    c.final_grade) >= 4.0 or c.alpha_final_grade == "A"])
            else:
                courses = []
                taken = 0
                approved = 0
            failed = taken - approved
            accumulated += approved
            percentage = accumulated * 100 / 16
            if accumulated == 16:
              self.requirements_ready = True
              self.requirements_ready_at = semester_number
            progresses.update(
                {semester: {
                    "semester": semester,
                    "percentage": percentage,
                    "approved": approved,
                    "failed": failed,
                    "taken": taken,
                    "accumulated": accumulated,
                    "total": 16,
                    "semester_start": start_timestamp,
                    "semester_end": end_timestamp,
                    "start_timestamp": timestamp_after(end_timestamp, 3),
                    "end_timestamp": timestamp_after(end_timestamp, 4),
                    "activity": get_activity(taken, approved, accumulated)
                }})
        return progresses


class Course:

    all = {}

    # format month/day
    timestamps = {
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

    def __init__(self, data):
        self.__dict__ = data
        self.course_id = "{}{}{}".format(
            data['rut'], data['initials'], data['semester'])
        self.case_id = ['student_number']
        self.student_id = "{}{}".format(
            data['student_number'], data['admission_year'])
        self.start_timestamp, self.end_timestamp = Course.timestamp_from_absolute(
            data['semester'], data['year'])
        self.grade = data['final_grade'] if data['final_grade'] != "nan" else data['alpha_final_grade']

        Course.all.update({self.course_id: self})

    @classmethod
    def filter_by(cls, field, value):
        return {k: v for k, v in cls.all.items() if getattr(v, field) == value}

    @classmethod
    def timestamp_from_relative(cls, relative_semester, admission_year):
        relative_semester = int(relative_semester)
        semester = 3 if relative_semester % 3 == 0 else relative_semester % 3
        start = cls.timestamps[semester]['start_date']
        end = cls.timestamps[semester]['end_date']
        year = int(admission_year) + int(relative_semester / 3)
        return ["{}/{}".format(year, start), "{}/{}".format(year, end)]

    @classmethod
    def timestamp_from_absolute(cls, absolute_semester, year):
        semester = int(absolute_semester)
        start = cls.timestamps[semester]['start_date']
        end = cls.timestamps[semester]['end_date']
        year = int(year) + int(semester / 3)
        return ["{}/{}".format(year, start), "{}/{}".format(year, end)]

    @classmethod
    def with_initials(cls, initials):
        return {k: v for k, v in cls.all.items() if v.initials in initials}

    @classmethod
    def from_students(cls, students):
        return {k: v for k, v in cls.all.items() if v.student_id in students}

    def __repr__(self):
        return "{}-{} {}-{}: {} ({})".format(self.year, self.semester, self.initials, self.section, self.course_name, self.grade)

    def relative_semester(self):
        relative_year = int(self.year) - int(self.admission_year)
        semester = relative_year * 3 + int(self.semester)
        return int(semester)


class Requirement:

    all = {}

    def __init__(self, **data):
        self.initials = data['initials']
        self.valid_initials = data['valid_initials'] + [self.initials]
        self.name = data['name']
        self.semester = data['semester']

        if self.valid_initials:
            for initial in self.valid_initials:
                Requirement.all.update({initial: self})


# class ProgressActivity:

    # JUST TO DUMP DATA!


class StudentRaw:
    all = []

    prop_names = {
        'RUT': 'rut',
        'N°ALUMNO': 'student_number',
        'CURRICULUM': 'curriculum',
        'CODIGO PROGRAMA': 'program_code',
        'PROGRAMA': 'program',
        'CODIGO PREFERENCIA ESPECIALIDAD': 'specialty_preference_code',
        'PREFERENCIA ESPECIALIDAD': 'specialty_preference',
        'CODIGO PREFERENCIA MAJOR': 'major_preference_code',
        'PREFERENCIA MAJOR': 'major_preference',
        'CODIGO MAJOR SELECCIONADO': 'selected_major_code',
        'MAJOR SELECCIONADO': 'selected_major',
        'CODIGO MINOR SELECCIONADO': 'selected_minor_code',
        'MINOR SELECCIONADO': 'selected_minor',
        'TRACK/ÁREA': 'track',
        'PLAN DE ESTUDIOS PERSONALIZADO': 'customized_studies_plan',
        'ESTADO': 'state',
        'AÑO INGRESO': 'admission_year',
        'VÍA DE INGRESO': 'admission_way',
        'TIPO INGRESO ESPECIAL': 'special_admission_type',
        'PROM. PPA': 'ppa',
        'TOTAL CRÉDITOS APROBADOS': 'total_approved_credits',
        'TOTAL CRÉDITOS CONVALIDADOS': 'total_validated_credits',
        'TOTAL CRÉDITOS APROBADOS+CONVALIDADOS': 'total_approved_and_validated_credits',
        'TOTAL CRÉDITOS REPROBADOS': 'total_failed_credits',
        'TOTAL CRÉDITOS INSCRITOS': 'total_enrolled_credits',
        'N° CAUSALES ELIMINACIÓN (POR SEMESTRE)': 'elimination_causals_number',
        'ESTUDIOS VIGENTES(PARALELO)': 'valid_studies',
        'ESTUDIOS NO VIGENTES(FINALIZADOS POR ALGÚN MOTIVO)': 'invalid_studies',
        'LICENCIADO': 'licensed',
        'FECHA LIC.': 'licensed_at',
        'EGRESADO': 'graduated',
        'FECHA EGR.': 'graduated_at',
        'TITULADO': 'tituled',
        'COLEGIO REGIÓN': 'school_region',
        'COLEGIO TIPO': 'school_type',
        'COLEGIO EGRESO': 'school_of_graduation',
        'ESTADO DSRD ACTUAL': 'dsrd_current_state',
        'TIPO INGRESO': 'admission_type',
        'PUESTO': 'admission_ranking',
    }

    def __init__(self, **kwargs):
        self.rut = str(kwargs.get('RUT', ''))
        self.student_number = str(kwargs.get('N°ALUMNO', ''))
        self.curriculum = str(kwargs.get('CURRICULUM', ''))
        self.program_code = str(kwargs.get('CODIGO PROGRAMA', ''))
        self.program = str(kwargs.get('PROGRAMA', ''))
        self.specialty_preference_code = str(kwargs.get(
            'CODIGO PREFERENCIA ESPECIALIDAD', ''))
        self.specialty_preference = str(kwargs.get(
            'PREFERENCIA ESPECIALIDAD', ''))
        self.major_preference_code = str(kwargs.get(
            'CODIGO PREFERENCIA MAJOR', ''))
        self.major_preference = str(kwargs.get('PREFERENCIA MAJOR', ''))
        self.selected_major_code = str(kwargs.get(
            'CODIGO MAJOR SELECCIONADO', ''))
        self.selected_major = str(kwargs.get('MAJOR SELECCIONADO', ''))
        self.selected_minor_code = str(kwargs.get(
            'CODIGO MINOR SELECCIONADO', ''))
        self.selected_minor = str(kwargs.get('MINOR SELECCIONADO', ''))
        self.track = str(kwargs.get('TRACK/ÁREA', ''))
        self.customized_studies_plan = str(kwargs.get(
            'PLAN DE ESTUDIOS PERSONALIZADO', ''))
        self.state = str(kwargs.get('ESTADO', ''))
        self.admission_year = str(kwargs.get('AÑO INGRESO', ''))
        self.admission_way = str(kwargs.get('VÍA DE INGRESO', ''))
        self.special_admission_type = str(
            kwargs.get('TIPO INGRESO ESPECIAL', ''))
        self.ppa = str(kwargs.get('PROM. PPA', ''))
        self.total_approved_credits = str(kwargs.get(
            'TOTAL CRÉDITOS APROBADOS', ''))
        self.total_validated_credits = str(kwargs.get(
            'TOTAL CRÉDITOS CONVALIDADOS', ''))
        self.total_approved_and_validated_credits = str(kwargs.get(
            'TOTAL CRÉDITOS APROBADOS+CONVALIDADOS', ''))
        self.total_failed_credits = str(kwargs.get(
            'TOTAL CRÉDITOS REPROBADOS', ''))
        self.total_enrolled_credits = str(kwargs.get(
            'TOTAL CRÉDITOS INSCRITOS', ''))
        self.elimination_causals_number = str(kwargs.get(
            'N° CAUSALES ELIMINACIÓN (POR SEMESTRE)', ''))
        self.valid_studies = str(kwargs.get('ESTUDIOS VIGENTES(PARALELO)', ''))
        self.invalid_studies = str(kwargs.get(
            'ESTUDIOS NO VIGENTES(FINALIZADOS POR ALGÚN MOTIVO)', ''))
        self.licensed = str(kwargs.get('LICENCIADO', ''))
        self.licensed_at = str(kwargs.get('FECHA LIC.', ''))
        self.graduated = str(kwargs.get('EGRESADO', ''))
        self.graduated_at = str(kwargs.get('FECHA EGR.', ''))
        self.tituled = str(kwargs.get('TITULADO', ''))
        self.school_region = str(kwargs.get('COLEGIO REGIÓN', ''))
        self.school_type = str(kwargs.get('COLEGIO TIPO', ''))
        self.school_of_graduation = str(kwargs.get('COLEGIO EGRESO', ''))
        self.dsrd_current_state = str(kwargs.get('ESTADO DSRD ACTUAL', ''))
        self.admission_type = str(kwargs.get('TIPO INGRESO', ''))
        self.admission_ranking = str(kwargs.get('PUESTO', ''))
        StudentRaw.all.append(self)


class CourseRaw:
    all = []

    prop_names = {
        'RUT': 'rut',
        'N°ALUMNO': 'student_number',
        'SEXO': 'sex',
        'AÑO ADMISIÓN': 'admission_year',
        'PROGRAMA CODIGO': 'program_code',
        'PROGRAMA': 'program',
        'MAJOR CODIGO SELECCIONADO': 'selected_major_code',
        'MAJOR SELECCIONADO': 'selected_major',
        'MAJOR TRACK/ÁREA ': 'track',
        'MINOR CODIGO SELECCIONADO': 'selected_minor_code',
        'MINOR SELECCIONADO': 'selected_minor',
        'CREDITOS ALUMNO': 'student_credits',
        'CURSO CURRICULUM': 'curriculum_course',
        'CURSO PROGRAMA': 'program_course',
        'AÑO': 'year',
        'SEMESTRE': 'semester',
        'SIGLA': 'initials',
        'SECCIÓN': 'section',
        'NOMBRE CURSO': 'course_name',
        'CREDITOS CURSO': 'course_credits',
        'NOTA FINAL': 'final_grade',
        'NOTA FINAL ALFA': 'alpha_final_grade',
        'PPA Global': 'global_ppa',
        'Estado en DARA': 'dara_state',
        'VIA INGRESO': 'admission_way',
        'VIA CASO INGRESO': 'admission_case_way',
    }

    def __init__(self, **kwargs):
        self.rut = str(kwargs.get('RUT', ''))
        self.student_number = str(kwargs.get('N°ALUMNO', ''))
        self.sex = str(kwargs.get('SEXO', ''))
        self.admission_year = str(kwargs.get('AÑO ADMISIÓN', ''))
        self.program_code = str(kwargs.get('PROGRAMA CODIGO', ''))
        self.program = str(kwargs.get('PROGRAMA', ''))
        self.selected_major_code = str(kwargs.get(
            'MAJOR CODIGO SELECCIONADO', ''))
        self.selected_major = str(kwargs.get('MAJOR SELECCIONADO', ''))
        self.track = str(kwargs.get('MAJOR TRACK/ÁREA ', ''))
        self.selected_minor_code = str(kwargs.get(
            'MINOR CODIGO SELECCIONADO', ''))
        self.selected_minor = str(kwargs.get('MINOR SELECCIONADO', ''))
        self.student_credits = str(kwargs.get('CREDITOS ALUMNO', ''))
        self.curriculum_course = str(kwargs.get('CURSO CURRICULUM', ''))
        self.program_course = str(kwargs.get('CURSO PROGRAMA', ''))
        self.year = str(kwargs.get('AÑO', ''))
        self.semester = str(kwargs.get('SEMESTRE', ''))
        self.initials = str(kwargs.get('SIGLA', ''))
        self.section = str(kwargs.get('SECCIÓN', ''))
        self.course_name = str(kwargs.get('NOMBRE CURSO', ''))
        self.course_credits = str(kwargs.get('CREDITOS CURSO', ''))
        self.final_grade = str(kwargs.get('NOTA FINAL', ''))
        self.alpha_final_grade = str(kwargs.get('NOTA FINAL ALFA', ''))
        self.global_ppa = str(kwargs.get('PPA Global', ''))
        self.dara_state = str(kwargs.get('Estado en DARA', ''))
        self.admission_way = str(kwargs.get('VIA INGRESO', ''))
        self.admission_case_way = str(kwargs.get('VIA CASO INGRESO', ''))
        CourseRaw.all.append(self)


if __name__ == '__main__':
    print("This module doesn't run code. Try running the 'main.py' file!")

    # for k, v in course_prop_names.items():
    #   print("self.{} = str(kwargs.get('{}', ''))".format(v, k))
