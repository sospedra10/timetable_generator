import pandas as pd
from datetime import datetime, timedelta
import itertools

# Load data from Excel
folder_data = 'data'
employee_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Employees')
vacation_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Vacation')

# Assuming the data structure:
# Employees sheet: 'Name'
# Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'


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

# Dictionary to store timetables for each employee
employee_timetables = {}

# List to store all employees
employees = list(employee_data['Name'])

# Dictionary to store vacation dates for each employee
employee_vacations = {name: [] for name in employees}
for index, row in vacation_data.iterrows():
    employee_vacations[row['Name']].extend(pd.date_range(start=row['Vacation Start'], end=row['Vacation End']).tolist())
print(employee_vacations)
print()

# Generating timetables for each day
start_date = datetime.now().date()
end_date = start_date + timedelta(days=7)  # Assuming 30 days timetable
current_date = start_date
while current_date < end_date:
    employee_timetables[current_date] = generate_daily_timetable(current_date, employees, employee_vacations)
    current_date += timedelta(days=1)

# Output timetable
print("Timetable:")
for date, timetable in employee_timetables.items():
    print(f"Date: {date}")
    for entry in timetable:
        print(f"Shift: {entry[2]}, Employee: {entry[1]}")


# Make a unique dataframe for all employees knowing when each person works
df = pd.DataFrame(columns=['Date', 'Employee', 'Shift'])
for date, timetable in employee_timetables.items():
    df = pd.concat([df, pd.DataFrame(timetable, columns=['Date', 'Employee', 'Shift'])])
print(df)


# Make another dataframe with column being Date and rows being the shift [Morning, Afternoon] and values the Employee names
df2 = df.pivot(index='Shift', columns='Date', values='Employee') 
# Make rows Morning, Afternoon in that order
df2 = df2.reindex(['Morning', 'Afternoon'])
# Modify the column names to be the date in the format 'DD/MM/YYYY'
df2.columns = [date.strftime('%d/%m/%Y') for date in df2.columns]
print(df2)

# Save timetable to Excel taking into account the multicolumn. Save it to a sheet called 'Timetable' in the file 'employee_data.xlsx'
with pd.ExcelWriter(f'{folder_data}/employee_data.xlsx', mode='a') as writer:
    df2.to_excel(writer, sheet_name='Timetable', index=True)
    print(df2)

# with pd.ExcelWriter(f'{folder_data}/timetable.xlsx') as writer:
#     df2.to_excel(writer, sheet_name='Timetable', index=True)
