import pandas as pd
from datetime import datetime, timedelta


# Load data from Excel
folder_data = 'data'
employee_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Employees')
vacation_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Vacation')

# Assuming the data structure:
# Employees sheet: 'Name'
# Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'

# Function to convert date strings to datetime objects
def str_to_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%Y')

# Convert vacation dates to datetime objects
vacation_data['Vacation Start'] = vacation_data['Vacation Start'].apply(str_to_date)
vacation_data['Vacation End'] = vacation_data['Vacation End'].apply(str_to_date)

# Function to generate timetable for each employee
def generate_timetable(employee_name, vacation_dates):
    timetable = []
    today = datetime.now().date()
    # Generating timetable for 5 working days per week
    for _ in range(5):
        # Check if the day falls within vacation period
        if today in vacation_dates:
            timetable.append((today, employee_name, "Vacation"))
        else:
            # Assuming two shifts: morning and afternoon
            timetable.append((today, employee_name, "Morning"))
            timetable.append((today, employee_name, "Afternoon"))
        today += timedelta(days=1)
    return timetable

# Dictionary to store timetables for each employee
employee_timetables = {}

# Generating timetables for each employee
for index, row in employee_data.iterrows():
    name = row['Name']
    # Get vacation dates for this employee
    vacation_dates = vacation_data[vacation_data['Name'] == name][['Vacation Start', 'Vacation End']]
    vacation_dates = [(start + timedelta(days=x)).date() for start, end in zip(vacation_dates['Vacation Start'], vacation_dates['Vacation End']) for x in range((end - start).days + 1)]
    # Generating timetable
    employee_timetables[name] = generate_timetable(name, vacation_dates)

# Output timetable
for name, timetable in employee_timetables.items():
    print(f"Timetable for {name}:")
    for entry in timetable:
        print(f"Date: {entry[0]}, Employee: {entry[1]}, Shift: {entry[2]}")
