class Student:

    all = []

    def __init__(self, data):
        self.__dict__ = data

    @classmethod
    def filter_by(cls, field, value):
        return list(filter(lambda s: getattr(s, field) == value, cls.all))


class CourseInstance:

    all = []

    def __init__(self, data):
        self.__dict__ = data

    @classmethod
    def filter_by(cls, field, value):
        return list(filter(lambda s: getattr(s, field) == value, cls.all))

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
        self.rut = kwargs.get('RUT', None)
        self.student_number = kwargs.get('N°ALUMNO', None)
        self.curriculum = kwargs.get('CURRICULUM', None)
        self.program_code = kwargs.get('CODIGO PROGRAMA', None)
        self.program = kwargs.get('PROGRAMA', None)
        self.specialty_preference_code = kwargs.get(
            'CODIGO PREFERENCIA ESPECIALIDAD', None)
        self.specialty_preference = kwargs.get(
            'PREFERENCIA ESPECIALIDAD', None)
        self.major_preference_code = kwargs.get(
            'CODIGO PREFERENCIA MAJOR', None)
        self.major_preference = kwargs.get('PREFERENCIA MAJOR', None)
        self.selected_major_code = kwargs.get(
            'CODIGO MAJOR SELECCIONADO', None)
        self.selected_major = kwargs.get('MAJOR SELECCIONADO', None)
        self.selected_minor_code = kwargs.get(
            'CODIGO MINOR SELECCIONADO', None)
        self.selected_minor = kwargs.get('MINOR SELECCIONADO', None)
        self.track = kwargs.get('TRACK/ÁREA', None)
        self.customized_studies_plan = kwargs.get(
            'PLAN DE ESTUDIOS PERSONALIZADO', None)
        self.state = kwargs.get('ESTADO', None)
        self.admission_year = kwargs.get('AÑO INGRESO', None)
        self.admission_way = kwargs.get('VÍA DE INGRESO', None)
        self.special_admission_type = kwargs.get('TIPO INGRESO ESPECIAL', None)
        self.ppa = kwargs.get('PROM. PPA', None)
        self.total_approved_credits = kwargs.get(
            'TOTAL CRÉDITOS APROBADOS', None)
        self.total_validated_credits = kwargs.get(
            'TOTAL CRÉDITOS CONVALIDADOS', None)
        self.total_approved_and_validated_credits = kwargs.get(
            'TOTAL CRÉDITOS APROBADOS+CONVALIDADOS', None)
        self.total_failed_credits = kwargs.get(
            'TOTAL CRÉDITOS REPROBADOS', None)
        self.total_enrolled_credits = kwargs.get(
            'TOTAL CRÉDITOS INSCRITOS', None)
        self.elimination_causals_number = kwargs.get(
            'N° CAUSALES ELIMINACIÓN (POR SEMESTRE)', None)
        self.valid_studies = kwargs.get('ESTUDIOS VIGENTES(PARALELO)', None)
        self.invalid_studies = kwargs.get(
            'ESTUDIOS NO VIGENTES(FINALIZADOS POR ALGÚN MOTIVO)', None)
        self.licensed = kwargs.get('LICENCIADO', None)
        self.licensed_at = kwargs.get('FECHA LIC.', None)
        self.graduated = kwargs.get('EGRESADO', None)
        self.graduated_at = kwargs.get('FECHA EGR.', None)
        self.tituled = kwargs.get('TITULADO', None)
        self.school_region = kwargs.get('COLEGIO REGIÓN', None)
        self.school_type = kwargs.get('COLEGIO TIPO', None)
        self.school_of_graduation = kwargs.get('COLEGIO EGRESO', None)
        self.dsrd_current_state = kwargs.get('ESTADO DSRD ACTUAL', None)
        self.admission_type = kwargs.get('TIPO INGRESO', None)
        self.admission_ranking = kwargs.get('PUESTO', None)
        StudentRaw.all.append(self)


class CourseInstanceRaw:
    all = []

    prop_names = {
        'RUT': 'rut',
        'N°ALUMNO': 'student_number',
        'SEXO': 'sexo',
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
        self.rut = kwargs.get('RUT', None)
        self.student_number = kwargs.get('N°ALUMNO', None)
        self.sexo = kwargs.get('SEXO', None)
        self.admission_year = kwargs.get('AÑO ADMISIÓN', None)
        self.program_code = kwargs.get('PROGRAMA CODIGO', None)
        self.program = kwargs.get('PROGRAMA', None)
        self.selected_major_code = kwargs.get(
            'MAJOR CODIGO SELECCIONADO', None)
        self.selected_major = kwargs.get('MAJOR SELECCIONADO', None)
        self.track = kwargs.get('MAJOR TRACK/ÁREA ', None)
        self.selected_minor_code = kwargs.get(
            'MINOR CODIGO SELECCIONADO', None)
        self.selected_minor = kwargs.get('MINOR SELECCIONADO', None)
        self.student_credits = kwargs.get('CREDITOS ALUMNO', None)
        self.curriculum_course = kwargs.get('CURSO CURRICULUM', None)
        self.program_course = kwargs.get('CURSO PROGRAMA', None)
        self.year = kwargs.get('AÑO', None)
        self.semester = kwargs.get('SEMESTRE', None)
        self.initials = kwargs.get('SIGLA', None)
        self.section = kwargs.get('SECCIÓN', None)
        self.course_name = kwargs.get('NOMBRE CURSO', None)
        self.course_credits = kwargs.get('CREDITOS CURSO', None)
        self.final_grade = kwargs.get('NOTA FINAL', None)
        self.alpha_final_grade = kwargs.get('NOTA FINAL ALFA', None)
        self.global_ppa = kwargs.get('PPA Global', None)
        self.dara_state = kwargs.get('Estado en DARA', None)
        self.admission_way = kwargs.get('VIA INGRESO', None)
        self.admission_case_way = kwargs.get('VIA CASO INGRESO', None)
        CourseInstanceRaw.all.append(self)


if __name__ == '__main__':
    print("This module doesn't run code. Try running the 'main.py' file!")

    # for k, v in course_prop_names.items():
    #   print("self.{} = kwargs.get('{}', None)".format(v, k))
