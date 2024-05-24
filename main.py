import pandas as pd
import streamlit as st
import time

from utils import generate_timetable, create_timetable_dataframe, get_employee_vacations, save_data
from employee_utils import add_employee, edit_employee
from vacations_utils import add_employee_vacation, edit_employee_vacation


st.set_page_config(layout="wide")
st.title('Employee Timetable Generator')

# Settings for generating timetable
st.sidebar.markdown('### Settings:')
days = st.sidebar.slider('Select number of days to generate timetable:', 1, 30, value=7, step=1)


# Load data from Excel
folder_data = 'data'
employee_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Employees')
vacation_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Vacation')
print(employee_data)
# vacation start and end without the time
vacation_data['Vacation Start'] = pd.to_datetime(vacation_data['Vacation Start']).dt.date
vacation_data['Vacation End'] = pd.to_datetime(vacation_data['Vacation End']).dt.date

# Assuming the data structure:
# Employees sheet: 'Name'
# Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'


tabs = ['Timetable', 'Shift Counts', 'Employees', 'Vacation']
timetable_tab, shift_counts_tab, employees_tab, vacations_tab = st.tabs(tabs)

# List to store all employees
st.session_state.employees = list(employee_data['Name'])
st.session_state.employees_estancos = employee_data
st.session_state.n_estancos = st.session_state.employees_estancos.shape[1] - 1




with employees_tab:
    st.write("#### Employees:")
    # Tranform employee dataset to a dataframe with employee names as "Name" columna and another column for the estancos he woorks in as a unique string as "1, 2, 4"
    employees_display_df = {}
    for i, employee in enumerate(st.session_state.employees):
        estancos = []
        for estanco in range(st.session_state.n_estancos):
            if st.session_state.employees_estancos[f'Estanco_{estanco+1}'].iloc[i] == 1:
                estancos.append(str(estanco+1))
        employees_display_df[employee] = ', '.join(estancos)
    
    employees_display_df = pd.DataFrame(employees_display_df.items(), columns=['Name', 'Estancos'])

    
    # Display employee data
    # st.dataframe(employee_data, use_container_width=True)

    add_employee_col, edit_employee_col, _ = st.columns([2, 2, 9])
    if add_employee_col.button('Add Employee'):
        add_employee(st, vacation_data, folder_data)
    if edit_employee_col.button('Edit Employee'):
        edit_employee(st, vacation_data, folder_data)

    st.dataframe(employees_display_df, use_container_width=True, hide_index=True, )

    # not at the moment (some errors)
    # employee_data = st.data_editor(employee_data.sort_values(by='Name'), hide_index=True, num_rows="dynamic")
    # # Save all data to Excel
    # save_data(folder_data, employee_data, vacation_data, timetable_data=None)




# Get vacation dates for each employee
employee_vacations = get_employee_vacations(st.session_state.employees, vacation_data)

# Vacation number of days from employee_vacations dictionary
vacation_data['Days'] = [(vacation_data.iloc[i]['Vacation End'] - vacation_data.iloc[i]['Vacation Start']).days+1 for i in range(len(vacation_data))]



with vacations_tab:
    st.write("#### Employee Vacations:")

    
    add_employee_vacation_col, edit_employee_vacation_col, _ = st.columns([2, 2, 9])
    if add_employee_vacation_col.button('Add Vacation'):
        add_employee_vacation(st, vacation_data, folder_data)
    if edit_employee_vacation_col.button('Edit Vacation'):
        edit_employee_vacation(st, vacation_data, folder_data)


    st.dataframe(vacation_data.sort_values(by='Name'), hide_index=True, use_container_width=True)  
    
    # Save all data to Excel
    # save_data(folder_data, employee_data, vacation_data, timetable_data=None)

    employee_vacations = get_employee_vacations(st.session_state.employees, vacation_data)

    # Plot vacation dates per employee
    st.write("#### Vacation Dates:")
    # pyplot chart
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.bar(employee_vacations.keys(), [len(vacations) for vacations in employee_vacations.values()])
    plt.xlabel('Employee')
    plt.ylabel('Number of vacations')
    # make the plot smaller
    # plt.gcf().set_size_inches(4, 2)
    a, plot, b = st.columns([2, 10, 2])
    plot.pyplot(plt)

    

get_timetables_button = st.sidebar.button('Get Timetables')
if get_timetables_button:
    # Generating timetables for each day
    # employee_timetables = generate_timetable(days=days, employees=employees, st.session_state.employees_estancos=st.session_state.employees_estancos, employee_vacations=employee_vacations)
    from utils import generate_optimized_timetable
    employee_timetables, score = generate_optimized_timetable(days, st.session_state.employees, st.session_state.employees_estancos, employee_vacations)

    from utils import count_shifts
    st.write(count_shifts(employee_timetables, type='unabailable'))

    print('----')
    print(employee_timetables)
    print('----')

    # Output timetable
    print("Timetable:")
    for estanco in range(st.session_state.n_estancos):
        print(f"Estanco {estanco+1}:")
        for date, timetable in employee_timetables[f'Estanco_{estanco+1}'].items():
            print(f"Date: {date}")
            for entry in timetable:
                print(f"Shift: {entry[2]}, Employee: {entry[1]}")


# tabular_data, timetable_data = create_timetable_dataframe(employee_timetables, folder_data=folder_data)

with timetable_tab:
    st.write("#### Timetables:")

    if get_timetables_button:

        estancos_timetables_df = []
        for estanco in range(st.session_state.n_estancos):
            tabular_data, timetable_data = create_timetable_dataframe(employee_timetables[f'Estanco_{estanco+1}'], folder_data=folder_data)
            estancos_timetables_df.append((tabular_data, timetable_data))

        for estanco in range(st.session_state.n_estancos):
            tabular_data, timetable_data = estancos_timetables_df[estanco]
            st.write(f"**Estanco {estanco+1}:**")
            # st.dataframe(tabular_data)
            st.dataframe(timetable_data)
        # st.dataframe(timetable_data)



# with shift_counts_tab:
#     # count number of shifts per employee and per shift
#     shift_counts = tabular_data.groupby(['Employee', 'Shift']).size().unstack().fillna(0)
#     shift_counts = shift_counts[['Morning', 'Afternoon']]
#     st.write("#### Shift Counts:")
#     st.write(shift_counts)

#     # Plot shift counts
#     st.bar_chart(shift_counts)


