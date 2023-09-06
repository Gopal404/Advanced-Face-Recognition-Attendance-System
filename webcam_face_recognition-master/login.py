import tkinter as tk
import pandas as pd
import os

# Create a new window
root = tk.Tk()

# Set the window title
root.title("Login Page - Automated Facial Recognition Attendance")
root.state('zoomed')
# Set the background color
root.configure(bg="#99b3ff")

# Set the font styles
title_font = ("Helvetica", 32, "bold")
label_font = ("Helvetica", 18, "bold")
text_font = ("Helvetica", 17)


# Create a frame for the login form
frame = tk.Frame(root, bg="white", padx=200, pady=120)

# Create a title label
title_label = tk.Label(frame, text="Admin Login", font=title_font, bg="#ffffff")

# Create labels and entry fields for username and password
username_label = tk.Label(frame, text="Username", font=label_font, bg="#ffffff")
username_entry = tk.Entry(frame, width=40, borderwidth=2, relief="groove", font=text_font)

password_label = tk.Label(frame, text="Password", font=label_font, bg="#ffffff")
password_entry = tk.Entry(frame, show="\u2022", width=40, borderwidth=2, relief="groove", font=text_font)


# Create a button to submit the login form
def login():
    email = username_entry.get()
    password = password_entry.get()
    
    # Load the admin data from CSV file
    a = pd.read_csv("admin.csv")
    
    # Check if email and password match
    for i in range(len(a)):
        e=str(a["Email"][i])
        p=str(a["Password"][i])
        if e == email and p == password:
            # Login successful
            result_label.config(text="Login Successful Please Wait", fg="green")
            name=(str(a["First_Name"][i])+" "+str(a["Last_Name"][i])) #Storing the name

            root.destroy()  # Close the login window
            os.system('python fronttest.py "{}" "{}"'.format(name,email))
            return
       
    # Login unsuccessful
    result_label.config(text="Invalid Email or Password", fg="red")
    
#Register    
register_label = tk.Label(frame, text="Not an Admin? Register Here", font=label_font, bg="#ffffff", fg="#2196f3", cursor="hand2")
def open_register():
    root.destroy() # Close the login window
    os.system('python regis.py')
register_label.bind("<Button-1>", lambda event: open_register())
register_label.grid(row=5, column=0, columnspan=2, padx=(90, 10), pady=10)
img = tk.PhotoImage(file="login.png")
submit_button = tk.Button(frame, text="Login", font=label_font, bg="#00bfff", padx=10, pady=3, cursor="hand2", command=login, bd=0, width=12, height=0)




# Create a label to display the result
result_label = tk.Label(frame, font=label_font, bg="#ffffff")

# Position the widgets on the frame
title_label.grid(row=0, column=0, columnspan=2, padx=(90, 10), pady=50)
username_label.grid(row=1, column=0, padx=5, pady=5)
username_entry.grid(row=1, column=1, padx=5, pady=5)
password_label.grid(row=2, column=0, padx=5, pady=5)
password_entry.grid(row=2, column=1, padx=5, pady=5)
submit_button.grid(row=3, column=0, columnspan=2, padx=(90, 10), pady=20)

result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Create a footer label
footer_label = tk.Label(root, text="Developed by Tanushree Sarkar & Gopal Sarkar.", font=("Helvetica", 10), bg="#f1f1f1")

# Position the footer label at the bottom of the window
footer_label.pack(side="bottom", fill="x", padx=10, pady=10)

# Pack the frame into the window
frame.pack()

# Run the main loop
root.mainloop()
