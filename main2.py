import pandas as pd
import streamlit as st

from utils import generate_timetable, create_timetable_dataframe


# Load data from Excel
folder_data = 'data'
employee_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Employees')
vacation_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Vacation')

# Assuming the data structure:
# Employees sheet: 'Name'
# Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'

# List to store all employees
employees = list(employee_data['Name'])

# Dictionary to store vacation dates for each employee
employee_vacations = {name: [] for name in employees}
for index, row in vacation_data.iterrows():
    employee_vacations[row['Name']].extend(pd.date_range(start=row['Vacation Start'], end=row['Vacation End']).tolist())
print(employee_vacations)
print()


# Generating timetables for each day
employee_timetables = generate_timetable(days=7, employees=employees, employee_vacations=employee_vacations)

# Output timetable
print("Timetable:")
for date, timetable in employee_timetables.items():
    print(f"Date: {date}")
    for entry in timetable:
        print(f"Shift: {entry[2]}, Employee: {entry[1]}")


timetable_data = create_timetable_dataframe(employee_timetables, folder_data=folder_data)
    


# with pd.ExcelWriter(f'{folder_data}/timetable.xlsx') as writer:
#     df2.to_excel(writer, sheet_name='Timetable', index=True)

