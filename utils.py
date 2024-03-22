from datetime import datetime, timedelta
import itertools
import pandas as pd



def get_employee_vacations(employees, vacation_data):
    # Dictionary to store vacation dates for each employee
    employee_vacations = {name: [] for name in employees}
    for index, row in vacation_data.iterrows():
        employee_vacations[row['Name']].extend(pd.date_range(start=row['Vacation Start'], end=row['Vacation End']).tolist())
    return employee_vacations


# Function to generate timetable for each day
def generate_daily_timetable(date, employees, vacation_dates):
    # convert date to datetime object
    date = datetime.strptime(str(date), '%Y-%m-%d')
    print('date:', date)
    daily_timetable = []
    for shift in ["Morning", "Afternoon"]:
        print('Shift:', shift)
        employee_assigned = False
        for employee in itertools.cycle(employees):
            print('Employee:', employee)
            employee_vacation_dates = vacation_dates[employee]
            print('employee_vacation_dates:', employee_vacation_dates)
            if date not in employee_vacation_dates:
                print('date not in employee_vacation_dates: No vacation: Assigned employee!')
                daily_timetable.append((date, employee, shift))
                # Remove assigned employee from the list because they can't work twice in a day
                employees.remove(employee)
                # Add assigned employee to the list of employees who have worked today to avoid assigning them again
                employees.append(employee)
                employee_assigned = True
                break
        if not employee_assigned:
            daily_timetable.append((date, "No available employee", shift))
    return daily_timetable



def generate_timetable(days, employees, employee_vacations):
    # Dictionary to store timetables for each employee
    employee_timetables = {}
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=days)
    current_date = start_date
    while current_date < end_date:
        employee_timetables[current_date] = generate_daily_timetable(current_date, employees, employee_vacations)
        current_date += timedelta(days=1)
    return employee_timetables


def create_timetable_dataframe(employee_timetables, folder_data=None):
    # Make a unique dataframe for all employees knowing when each person works
    df = pd.DataFrame(columns=['Date', 'Employee', 'Shift'])
    for date, timetable in employee_timetables.items():
        df = pd.concat([df, pd.DataFrame(timetable, columns=['Date', 'Employee', 'Shift'])])

    # Make another dataframe with column being Date and rows being the shift [Morning, Afternoon] and values the Employee names
    timetable_data = df.pivot(index='Shift', columns='Date', values='Employee') 
    # Make rows Morning, Afternoon in that order
    timetable_data = timetable_data.reindex(['Morning', 'Afternoon'])
    # Modify the column names to be the date in the format 'DD/MM/YYYY'
    timetable_data.columns = [date.strftime('%d/%m/%Y') for date in timetable_data.columns]

    # if folder_data:
        # Save timetable to Excel taking into account the multicolumn. Save it to a sheet called 'Timetable' in the file 'employee_data.xlsx'
        # with pd.ExcelWriter(f'{folder_data}/employee_data.xlsx', mode='a') as writer:
        #     timetable_data.to_excel(writer, sheet_name='Timetable', index=True)
    return timetable_data