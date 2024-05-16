import streamlit as st
import pandas as pd
from utils import save_data


@st.experimental_dialog("Add employee:")
def add_employee(st, employees, n_estancos, vacation_data, folder_data):
    "Dialog to add a new employee to the system."
    new_employee_name = st.text_input('**Name:**')
    st.write('**Estancos:**')
    new_employee_estancos = [st.checkbox(f'Estanco {i+1}') for i in range(n_estancos)]

    if st.button('Submit'):
        if new_employee_name in employees:
            st.error(f"Employee {new_employee_name} already exists")
            return
        if len(new_employee_name) == 0:
            st.error("Employee name can't be empty")
            return
        if not any(new_employee_estancos):
            st.error("Employee must work in at least one estanco")
            return
        employees.append(new_employee_name)
        new_employee = pd.DataFrame({'Name': new_employee_name, **{f'Estanco_{i+1}': int(new_employee_estancos[i]) for i in range(n_estancos)}}, index=[0])
        st.session_state.employees_estancos = pd.concat([st.session_state.employees_estancos, new_employee], ignore_index=True)
        st.success(f"Added new employee: {new_employee_name}")
        save_data(folder_data, st.session_state.employees_estancos, vacation_data, timetable_data=None)

        st.rerun()


@st.experimental_dialog("Edit employee:")
def edit_employee(st, employees, n_estancos, vacation_data, folder_data):
    "Dialog to edit an existing employee in the system."
    employee_name = st.selectbox('Select employee:', employees)
    employee_data = st.session_state.employees_estancos[st.session_state.employees_estancos['Name'] == employee_name].iloc[0]
    # Modify name
    new_employee_name = st.text_input('**Name:**', value=employee_name)
    estancos = [employee_data[f'Estanco_{i+1}'] for i in range(n_estancos)]
    st.write('**Estancos:**')
    new_employee_estancos = [st.checkbox(f'Estanco {i+1}', value=estancos[i])*1 for i in range(n_estancos)]

    if st.button('Submit'):
        if not any(new_employee_estancos):
            st.error("Employee must work in at least one estanco")
            return
        if new_employee_name != employee_name:
            if new_employee_name in employees:
                st.error(f"Employee {new_employee_name} already exists")
                return
            # Update employee name in the list of employees
        employees[employees.index(employee_name)] = new_employee_name
        st.session_state.employees_estancos.loc[st.session_state.employees_estancos['Name'] == employee_name, 'Name'] = new_employee_name
        st.session_state.employees_estancos.loc[st.session_state.employees_estancos['Name'] == employee_name, [f'Estanco_{i+1}' for i in range(n_estancos)]] = new_employee_estancos
        st.success(f"Edited employee: {employee_name}")

        save_data(folder_data, st.session_state.employees_estancos, vacation_data, timetable_data=None)
        st.rerun()