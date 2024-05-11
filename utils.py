from datetime import datetime, timedelta
import itertools
import pandas as pd



def get_employee_vacations(employees, vacation_data):
    # Dictionary to store vacation dates for each employee
    employee_vacations = {name: [] for name in employees}
    for index, row in vacation_data.iterrows():
        if row['Name'] is not None:
            employee_vacations[row['Name']].extend(pd.date_range(start=row['Vacation Start'], end=row['Vacation End']).tolist())
    return employee_vacations


def employee_is_free(estanco, employee, original_date, employee_timetables, daily_timetable):
    print('daily timetable', daily_timetable)

    # daily timetable [(datetime.datetime(2024, 5, 17, 0, 0), 'Mario', 'Morning')]
    # First, check if the employee is already assigned to work on the date for not working twice ont he same day
    if len(daily_timetable) > 0 and daily_timetable[0][1] == employee:
        return False

    for estanco_name, timetable in employee_timetables.items():
        if estanco_name != estanco:
            print('estanco_name:', estanco_name, original_date)
            print(timetable)
            if original_date in timetable:
                for entry in timetable[original_date]:
                    print('entry:', entry)
                    print(entry[1], employee)
                    if entry[1] == employee:  # if employee is already assigned to work on the date: continue
                        return False
        print()
    return True


# Function to generate timetable for each day
def generate_daily_timetable(original_date, employees, employees_estancos, vacation_dates, employee_timetables, estanco):
    print('Estanco:', estanco)
    # convert date to datetime object
    date = datetime.strptime(str(original_date), '%Y-%m-%d')
    # print('date:', date)
    daily_timetable = []
    for shift in ["Morning", "Afternoon"]:
        # print('Shift:', shift)
        employee_assigned = False
        for employee in employees:
            if employees_estancos[employees_estancos['Name'] == employee][estanco].values[0] == 0: # if employee can't work in the estanco: continue
                continue

            # Find if employee is available to work on the date or it is already assigned to work on the date on another estanco
            
            if not employee_is_free(estanco, employee, original_date, employee_timetables, daily_timetable):
                print('Employee is not free')
                continue

            
            employee_vacation_dates = vacation_dates[employee]
            if date not in employee_vacation_dates:
                daily_timetable.append((date, employee, shift))
                # Remove assigned employee from the list because they can't work twice in a day
                employees.remove(employee)
                # Add assigned employee to the list of employees who have worked today to avoid assigning them again
                employees.append(employee)
                employee_assigned = True
                break
        if not employee_assigned:
            daily_timetable.append((date, "No available employee", shift))
            print('No available employee!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return daily_timetable



def generate_timetable(days, employees, employees_estancos, employee_vacations):
    # Dictionary to store timetables for each employee
    employee_timetables = {}
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=days)
    current_date = start_date


    while current_date < end_date:
        print('current_date:', current_date)
        print('employees:', employees)
        print()

        for estanco in range(employees_estancos.shape[1] - 1):
    #     employees_estanco = employees_estancos[:, estanco]
            estanco_name = f'Estanco_{estanco+1}'
            if estanco_name not in employee_timetables:
                employee_timetables[estanco_name] = {}
            
            employee_timetables[estanco_name][current_date] = generate_daily_timetable(current_date, employees, employees_estancos, employee_vacations, employee_timetables, estanco_name) 
        # break
        current_date += timedelta(days=1)
    print('current_date:', current_date)
    print('employees:', employees)
    return employee_timetables


def create_timetable_dataframe(employee_timetables, folder_data=None):
    # Make a unique dataframe for all employees knowing when each person works
    tabular_data = pd.DataFrame(columns=['Date', 'Employee', 'Shift'])
    for date, timetable in employee_timetables.items():
        tabular_data = pd.concat([tabular_data, pd.DataFrame(timetable, columns=['Date', 'Employee', 'Shift'])])

    # Make another dataframe with column being Date and rows being the shift [Morning, Afternoon] and values the Employee names
    timetable_data = tabular_data.pivot(index='Shift', columns='Date', values='Employee') 
    # Make rows Morning, Afternoon in that order
    timetable_data = timetable_data.reindex(['Morning', 'Afternoon'])
    # Modify the column names to be the date in the format 'DD/MM/YYYY'
    timetable_data.columns = [date.strftime('%d/%m/%Y') for date in timetable_data.columns]

    # if folder_data:
        # Save timetable to Excel taking into account the multicolumn. Save it to a sheet called 'Timetable' in the file 'employee_data.xlsx'
        # with pd.ExcelWriter(f'{folder_data}/employee_data.xlsx', mode='a') as writer:
        #     timetable_data.to_excel(writer, sheet_name='Timetable', index=True)
    return tabular_data, timetable_data


def save_data(folder_data, employee_data, vacation_data, timetable_data):
    with pd.ExcelWriter(f'{folder_data}/employee_data.xlsx') as writer:
        employee_data.to_excel(writer, sheet_name='Employees', index=False)
        vacation_data.to_excel(writer, sheet_name='Vacation', index=False)
        if timetable_data is not None:
            timetable_data.to_excel(writer, sheet_name='Timetable', index=True)