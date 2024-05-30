from streamlit import experimental_dialog
import pandas as pd
from utils import save_data


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
        # Checking if the new vacation is inside the range of the employee vacation
        if (employee_vacation['Vacation Start'] <= new_vacation_start <= employee_vacation['Vacation End']) | (employee_vacation['Vacation Start'] <= new_vacation_end <= employee_vacation['Vacation End']):
            return True
        # Checking if the vacation is inside the range of the new vacation
        if (new_vacation_start <= employee_vacation['Vacation Start'] <= new_vacation_end) | (new_vacation_start <= employee_vacation['Vacation End'] <= new_vacation_end):
            return True
    return False


def check_vacation_errors(st, employee_name, employee_vacations, new_vacation_start, new_vacation_end):
    """
    Check if there are any errors with the new vacation dates.

    Parameters:
        st (streamlit): Streamlit object.
        employee_name (str): Name of the employee.
        employee_vacations (pd.DataFrame): DataFrame with the employee vacations.
        new_vacation_start (pd.Timestamp): Start date of the new vacation.
        new_vacation_end (pd.Timestamp): End date of the new vacation.

    Returns:
        bool: True if there is an error, False otherwise.
    """

    # Check if the new employee vacations are not collapsing with other vacations
    if are_vacation_collisions(employee_vacations, new_vacation_start, new_vacation_end):
        st.error(f"Employee {employee_name} already has a vacation in that period")
        return True
    if new_vacation_start > new_vacation_end:
        st.error("Vacation start date must be before vacation end date")
        return True
    return False


@experimental_dialog("Add employee vacation:")
def add_employee_vacation(st, vacation_data, folder_data):
    "Dialog to add a new employee vacation to the system."
    new_employee_name = st.selectbox('**Name:**', st.session_state.employees)
    new_vacation_start_col, new_vacation_end_col = st.columns(2)
    new_vacation_start = new_vacation_start_col.date_input('**Vacation Start:**')
    new_vacation_end = new_vacation_end_col.date_input('**Vacation End:**')

    employee_vacations = vacation_data[vacation_data['Name'] == new_employee_name]
    # Display employee vacations if they exist for the selected employee
    if employee_vacations.shape[0] > 0:
        st.write(employee_vacations)
    else:
        st.write("**No vacations for this employee at the moment**")

    if st.button('Submit'):
        
        if check_vacation_errors(st, new_employee_name, employee_vacations, new_vacation_start, new_vacation_end):
            return

        # Add new vacation to the vacation_data DataFrame
        new_vacation = pd.DataFrame({'Name': new_employee_name, 'Vacation Start': new_vacation_start, 'Vacation End': new_vacation_end}, index=[0])
        vacation_data = pd.concat([vacation_data, new_vacation], ignore_index=True)
        
        st.success(f"Added new vacation for {new_employee_name} successfully!")

        save_data(folder_data, st.session_state.employees_estancos, vacation_data, timetable_data=None)
        st.rerun()


@experimental_dialog("Edit employee vacation:")
def edit_employee_vacation(st, vacation_data, folder_data):
    "Dialog to edit an existing employee vacation in the system."
    employee_name = st.selectbox('Select vacation employee name to edit:', vacation_data['Name'].unique()) 

    employee_vacations = vacation_data[vacation_data['Name'] == employee_name]

    # Display employee vacations
    st.write(employee_vacations)

    # Select vacation to edit
    vacation_index = st.selectbox('Select vacation:', employee_vacations.index, format_func=lambda x: f"{employee_vacations.loc[x, 'Vacation Start']} to {employee_vacations.loc[x, 'Vacation End']}")

    selected_vacation = employee_vacations.loc[vacation_index]

    new_vacation_start_col, new_vacation_end_col = st.columns(2)
    new_vacation_start = new_vacation_start_col.date_input("**Vacation Start:**", selected_vacation['Vacation Start'])
    new_vacation_end = new_vacation_end_col.date_input("**Vacation End:**", selected_vacation['Vacation End'])
  

    if st.button('Submit'):
        # Check errors with the new vacation dates only if they are different from the current ones (employee_vacations would not include the selected vacation in this case)
        if check_vacation_errors(st, employee_name, employee_vacations.drop(vacation_index), new_vacation_start, new_vacation_end):
            return
        
        vacation_data.loc[vacation_index, 'Vacation Start'] = new_vacation_start
        vacation_data.loc[vacation_index, 'Vacation End'] = new_vacation_end
        
        st.success("Vacation updated successfully!")

        save_data(folder_data, st.session_state.employees_estancos, vacation_data, timetable_data=None)
        st.rerun()


@experimental_dialog("Delete employee vacation:")
def delete_employee_vacation(st, vacation_data, folder_data):
    "Dialog to delete an existing employee vacation in the system."
    employee_name = st.selectbox('Select vacation employee name to delete:', vacation_data['Name'].unique()) 

    employee_vacations = vacation_data[vacation_data['Name'] == employee_name]

    # Display employee vacations
    st.write(employee_vacations)

    # Select vacation to delete
    vacation_index = st.selectbox('Select vacation:', employee_vacations.index, format_func=lambda x: f"{employee_vacations.loc[x, 'Vacation Start']} to {employee_vacations.loc[x, 'Vacation End']}")

    if st.button('Delete'):
        vacation_data.drop(vacation_index, inplace=True)
        st.success("Vacation deleted successfully!")

        save_data(folder_data, st.session_state.employees_estancos, vacation_data, timetable_data=None)
        st.rerun()