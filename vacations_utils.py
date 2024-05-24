from streamlit import experimental_dialog
import pandas as pd


def are_vacation_collisions(employee_vacations, new_vacation_start, new_vacation_end):
    """
    Check if the new vacation dates are colliding with other vacations.

    Parameters:
    employee_vacations (pd.DataFrame): DataFrame with the employee vacations.
    new_vacation_start (pd.Timestamp): Start date of the new vacation.
    new_vacation_end (pd.Timestamp): End date of the new vacation.

    Returns:
    bool: True if there is a collision, False otherwise.
    
    
    """

    for _, employee_vacation in employee_vacations.iterrows():
        print()
        print(employee_vacation)
        print()
        print(new_vacation_start, new_vacation_end)
        print()
        
        print()
        # Checking if the new vacation is inside the range of the employee vacation
        if (employee_vacation['Vacation Start'] <= new_vacation_start <= employee_vacation['Vacation End']) | (employee_vacation['Vacation Start'] <= new_vacation_end <= employee_vacation['Vacation End']):
            return True
        # Checking if the vacation is inside the range of the new vacation
        if (new_vacation_start <= employee_vacation['Vacation Start'] <= new_vacation_end) | (new_vacation_start <= employee_vacation['Vacation End'] <= new_vacation_end):
            return True
    return False


@experimental_dialog("Add employee vacation:")
def add_employee_vacation(st, vacation_data, folder_data):
    "Dialog to add a new employee vacation to the system."
    new_employee_name = st.selectbox('**Name:**', st.session_state.employees)
    new_vacation_start = st.date_input('**Vacation Start:**')
    new_vacation_end = st.date_input('**Vacation End:**')

    employee_vacations = vacation_data[vacation_data['Name'] == new_employee_name]
    if employee_vacations.shape[0] > 0:
        st.write(employee_vacations)
    else:
        st.write("**No vacations for this employee at the moment**")

    # if new_vacation_start > new_vacation_end:
    #     st.warning("Vacation start date must be before vacation end date")

    if st.button('Submit'):
        # Check if the new employee vacations are not collapsing with other vacations
        if are_vacation_collisions(employee_vacations, new_vacation_start, new_vacation_end):
            st.error(f"Employee {new_employee_name} already has a vacation in that period")
            return
        if new_vacation_start > new_vacation_end:
            st.error("Vacation start date must be before vacation end date")
            return
        new_vacation = pd.DataFrame({'Name': new_employee_name, 'Vacation Start': new_vacation_start, 'Vacation End': new_vacation_end}, index=[0])
        vacation_data = pd.concat([vacation_data, new_vacation], ignore_index=True)
        
        st.success(f"Added new vacation for {new_employee_name}")

        st.write(vacation_data)

        # save_data(folder_data, st.session_state.employees_estancos, vacation_data, timetable_data=None)
        # st.rerun()

@experimental_dialog("Edit employee vacation:")
def edit_employee_vacation(st, vacation_data, folder_data):
    "Dialog to edit an existing employee vacation in the system."
    vacation_index = st.selectbox('Select vacation:', vacation_data[['Name', 'Vacation Start', 'Vacation End']].apply(lambda x: f"{x['Name']} : ({x['Vacation Start']} to {x['Vacation End']})", axis=1).tolist())
    vacation_employee_name = vacation_index.split(':')[0].strip()
    vacations_part = vacation_index.split('(')[1].split('to')
    vacation_start = pd.Timestamp(vacations_part[0].strip())
    vacation_end = pd.Timestamp(vacations_part[1].strip())
    st.write(vacation_employee_name, vacation_start, vacation_end)
    vacation_data = vacation_data[vacation_data['Name'] == vacation_index].iloc[0]
    # Modify name
    new_employee_name = st.selectbox('**Name:**', st.session_state.employees, index=st.session_state.employees.index(vacation_data['Name']))
    new_vacation_start = st.date_input('**Vacation Start:**', value=vacation_data['Vacation Start'])
    new_vacation_end = st.date_input('**Vacation End:**', value=vacation_data['Vacation End'])

    if st.button('Submit'):
        if new_vacation_start >= new_vacation_end:
            st.error("Vacation start date must be before vacation end date")
            return
        vacation_data['Name'] = new_employee_name
        vacation_data['Vacation Start'] = new_vacation_start
        vacation_data['Vacation End'] = new_vacation_end
        st.success(f"Edited vacation for {new_employee_name}")

        st.write(vacation_data)

        # save_data(folder_data, st.session_state.employees_estancos, vacation_data, timetable_data=None)
        # st.rerun()