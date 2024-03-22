from datetime import datetime
import itertools

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