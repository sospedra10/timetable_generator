import pandas as pd
import streamlit as st

from utils import generate_timetable, create_timetable_dataframe, get_employee_vacations


st.set_page_config(layout="wide")
st.title('Employee Timetable Generator')
# select days for which to generate timetable
days = st.slider('Select number of days to generate timetable:', 1, 30, value=7, step=1)


# Load data from Excel
folder_data = 'data'
employee_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Employees')
vacation_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Vacation')

# Assuming the data structure:
# Employees sheet: 'Name'
# Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'


tabs = ['Timetable', 'Shift Counts', 'Employees', 'Vacation']
timetable_tab, shift_counts_tab, employees_tab, vacations_tab = st.tabs(tabs)

# List to store all employees
employees = list(employee_data['Name'])

with employees_tab:
    st.write("#### Employees:")
    st.write(', '.join(employees))


# Get vacation dates for each employee
employee_vacations = get_employee_vacations(employees, vacation_data)

with vacations_tab:
    st.write("#### Employee Vacations:")
    for employee, vacations in employee_vacations.items():
        st.write(f"**{employee}**: {', '.join([str(vacation)[:10] for vacation in vacations])}")

    # Plot vacation dates per employee
    st.write("#### Vacation Dates:")
    st.bar_chart({employee: len(vacations) for employee, vacations in employee_vacations.items()})
    

# Generating timetables for each day
employee_timetables = generate_timetable(days=days, employees=employees, employee_vacations=employee_vacations)

# Output timetable
print("Timetable:")
for date, timetable in employee_timetables.items():
    print(f"Date: {date}")
    for entry in timetable:
        print(f"Shift: {entry[2]}, Employee: {entry[1]}")

tabular_data, timetable_data = create_timetable_dataframe(employee_timetables, folder_data=folder_data)

with timetable_tab:
    st.write("#### Timetable:")
    st.dataframe(timetable_data)

# count number of shifts per employee and per shift
shift_counts = tabular_data.groupby(['Employee', 'Shift']).size().unstack().fillna(0)
# shift_counts = shift_counts[['Employee', 'Morning', 'Afternoon']]

with shift_counts_tab:
    st.write("#### Shift Counts:")
    st.write(shift_counts)

    # Plot shift counts
    st.bar_chart(shift_counts)


