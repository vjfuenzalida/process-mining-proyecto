# Import pandas
import pandas as pd


def open_excel(path_to_excel):
    print("="*67)
    print("=== Reading file at '{}' with pandas library\t===".format(path_to_excel))
    file = path_to_excel
    xl = pd.ExcelFile(file)
    main_sheet = xl.sheet_names[0]
    df = xl.parse(main_sheet)
    print("=== Success! Loaded '{}' as pandas.DataFrame\t===".format(path_to_excel))
    return df


if __name__ == '__main__':
    print("This module doesn't run code. Try running the 'main.py' file!")
