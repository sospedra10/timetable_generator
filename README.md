# Employee Timetable Generator

This is a Streamlit web application for generating timetables for employees, considering their vacation days. 

## Usage

1. Run the Streamlit app:
   
streamlit run app.py

2. Use the slider to select the number of days for which you want to generate the timetable.

3. View employees and their vacations in the respective expanders.

4. View the generated timetable and shift counts.

## Data

The application expects employee and vacation data in Excel format.

- \`employee_data.xlsx\`: Contains information about employees.
- \`vacation_data.xlsx\`: Contains vacation dates for employees.

### Structure

- Employees sheet: 'Name'
- Vacation sheet: 'Name', 'Vacation Start', 'Vacation End'

## Dependencies

- pandas
- streamlit

## Installation

1. Clone the repository:

git clone https://github.com/sospedra10/employee-timetable-generator.git

2. Install dependencies:

pip install -r requirements.txt


## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

