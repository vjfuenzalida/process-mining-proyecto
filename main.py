from reader import open_excel

if __name__ == '__main__':

    years = [2013, 2014, 2015, 2016]

    def students_ext(year): return 'data/alumnos{}.xlsx'.format(year)

    def courses_ext(year): return 'data/cursos{}.xlsx'.format(year)

    students_files = {year: students_ext(year) for year in years}

    courses_files = {year: courses_ext(year) for year in years}

    students_data = {}
    courses_data = {}

    # print(students_files)
    # print(students_files)

    # for year in years:
    #     students_data[year] = open_excel(students_files[year])
    #     courses_data[year] = open_excel(courses_files[year])

    for year in years:
        students_data[year] = open_excel(students_files[year])
        courses_data[year] = open_excel(courses_files[year])

    print(students_data[year].columns)
    print(courses_data[year].columns)
