import pandas as pd
from datetime import datetime, timedelta



# Make another dataframe with columns being (Date, Shift) using  multicolumn and rows being the Employee names timetable
# df2 = df.pivot(index='Employee', columns=['Date', 'Shift'], values='Employee').fillna('-')


# Load data from Excel
folder_data = 'data'
employee_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Employees')
vacation_data = pd.read_excel(f'{folder_data}/employee_data.xlsx', sheet_name='Vacation')
print('Data loaded successfully!')

# Assuming the data structure:
# Employees sheet: 'Name'
# Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'


# Function to generate timetable for each employee
def generate_timetable(employee_name, vacation_dates):
    timetable = []
    today = datetime.now().date()
    print()
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

print(employee_timetables)
# Output timetable
print("Timetable:")
for i in range(5):
    for shift in ["Morning", "Afternoon"]:
        for name, timetable in employee_timetables.items():
            if timetable:
                entry = timetable.pop(0)
                if entry[2] != "Vacation":
                    print(f"Date: {entry[0]}, Shift: {entry[2]}, Employee: {entry[1]}")
                    break




# Save timetable to Excel
# with pd.ExcelWriter(f'{folder_data}/timetable.xlsx') as writer:
#     for name, timetable in employee_timetables.items():
#         df = pd.DataFrame(timetable, columns=['Date', 'Employee', 'Shift'])
#         df.to_excel(writer, sheet_name=name, index=False)
#         print(df)
        

# Create a unique dataframe for all employees knowing when each person works
df = pd.DataFrame(columns=['Date', 'Employee', 'Shift'])
for name, timetable in employee_timetables.items():
    df = df._append(pd.DataFrame(timetable, columns=['Date', 'Employee', 'Shift']))

print(df)
# Save timetable to Excel
# df.to_excel(f'{folder_data}/timetable.xlsx', index=False)   


