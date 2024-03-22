import pandas as pd
import streamlit as st

from utils import generate_timetable, create_timetable_dataframe, get_employee_vacations


st.set_page_config(layout="wide")
st.title('Employee Timetable Generator')
# select days for which to generate timetable
days = st.slider('Select number of days to generate timetable:', 1, 30, 1)


# Load data from Excel
folder_data = 'data'
employee_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Employees')
vacation_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Vacation')

# Assuming the data structure:
# Employees sheet: 'Name'
# Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'

# List to store all employees
employees = list(employee_data['Name'])

# Get vacation dates for each employee
employee_vacations = get_employee_vacations(employees, vacation_data)

# Generating timetables for each day
employee_timetables = generate_timetable(days=7, employees=employees, employee_vacations=employee_vacations)

# Output timetable
print("Timetable:")
for date, timetable in employee_timetables.items():
    print(f"Date: {date}")
    for entry in timetable:
        print(f"Shift: {entry[2]}, Employee: {entry[1]}")


timetable_data = create_timetable_dataframe(employee_timetables, folder_data=folder_data)
    
st.dataframe(timetable_data)
