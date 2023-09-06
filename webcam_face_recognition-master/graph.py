import matplotlib.pyplot as plt
from datetime import date
def show_attendance():
    # Retrieve the selected date
    date_str = get_date()

    # Convert the date string to a datetime object
    date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
    formatted_date = date.strftime('%d-%m-%Y')

    # Search the attendance records for the given date
    with open('StudentDetails/Attendance.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader) # skip the header row
        date_index = header.index(formatted_date+'_IN') if formatted_date+'_IN' in header else -1
        if date_index == -1:
            records_text.insert(tk.END, "No Records Found For The Given Date.")
        else:
            records_text.insert(tk.END, "Attendance Records For: " + date_str  + ":\n")

            # Create empty lists for student names and time differences
            student_names = []
            time_diffs = []

            for row in reader:
                if row[date_index]!='':
                    student_names.append(row[2])
                    time_in = datetime.datetime.strptime(row[date_index], '%H:%M:%S')
                    time_out = datetime.datetime.strptime(row[date_index+1], '%H:%M:%S')
                    time_diff = (time_out - time_in).total_seconds() / 3600  # convert to hours
                    time_diffs.append(time_diff)

            # Create a bar chart using matplotlib
            fig, ax = plt.subplots()
            ax.bar(student_names, time_diffs)
            ax.set_xlabel('Student Name')
            ax.set_ylabel('Time Spent (hours)')
            ax.set_title('Attendance Record for ' + formatted_date)
            plt.xticks(rotation=90)
            plt.show()
