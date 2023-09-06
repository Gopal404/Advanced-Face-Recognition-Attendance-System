import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
global email
global first_name
global last_name

def register():
    global email
    global first_name
    global last_name

    # get input values
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    password = entry_password.get()
    re_password = entry_re_password.get()
    # validate input values
    if not first_name:
        messagebox.showerror("Error", "Please enter your first name")
        return
    if not last_name:
        messagebox.showerror("Error", "Please enter your last name")
        return
    if not email:
        messagebox.showerror("Error", "Please enter your email")
        return
    if not password:
        messagebox.showerror("Error", "Please enter a password")
        return
    if password != re_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    # create new user account (add your own code here)
    data = {'First_Name': [first_name],
            'Last_Name': [last_name],
            'Email': [email],
            'Password': [password]}
    df = pd.DataFrame(data)
    df.to_csv('admin.csv', mode='a', header=not os.path.exists('admin.csv'), index=False)

    # clear input fields
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_re_password.delete(0, tk.END)

    # update status label
    messagebox.showinfo("Success", "Registration Successful")
    return email

# create a window
window = tk.Tk()
window.title("Admin Registration Page")
window.state('zoomed')  # maximize window
window.configure(bg="#99b3ff" )

# create a frame
frame = tk.Frame(window, bg="#f1f1f1", padx=100, pady=100)


# create labels and entry fields
label_title = tk.Label(frame, text="Admin Registration", font=("Arial", 32,"bold"))
label_title1 = tk.Label(frame, text="", font=("Arial", 20))
font_style = ("Arial", 16)
label_first_name = tk.Label(frame, text="First Name:", font=font_style)
entry_first_name = tk.Entry(frame, width=40, font=font_style, borderwidth=2, relief="groove",)
label_last_name = tk.Label(frame, text="Last Name:", font=font_style)
entry_last_name = tk.Entry(frame, width=40, font=font_style,borderwidth=2, relief="groove",)
label_email = tk.Label(frame, text="Email:", font=font_style)
entry_email = tk.Entry(frame, width=40, font=font_style,borderwidth=2, relief="groove",)
label_password = tk.Label(frame, text="Password:", font=font_style)
entry_password = tk.Entry(frame, show="\u2022", width=40, font=font_style,borderwidth=2, relief="groove",)
label_re_password = tk.Label(frame, text="Re-enter Password:", font=font_style)
entry_re_password = tk.Entry(frame, show="\u2022", width=40, font=font_style,borderwidth=2, relief="groove",)


def OTP():
    register()
    global first_name
    global last_name
    global email
    command = 'python OTP.py "{}" "{}" "{}"'.format(email, first_name, last_name)
    os.system(command)
    
    # print(email)
# create buttons
button_verify = tk.Button(frame, text="Register And Verify", command=OTP, foreground='white',background='green',activeforeground='red',activebackground='blue', font=font_style, width=18,height=1,cursor="hand2",bd=0)


button_register = tk.Button(frame, text="Register Only", command=register, bg="#0077CC", fg="white", font=font_style, width=18, height=1, cursor="hand2",activebackground="#005EA8",bd=0)
button_register.place(x=226,y=366)

label_font = ("Helvetica", 14, "bold")
register_label = tk.Label(frame, text="Already Registred? Login Here", font=label_font, fg="#2196f3", cursor="hand2")
def open_login():
    window.destroy() # Close the login window
    os.system('python login.py')


def show_tooltip(event):
    button_verify.tooltip = tk.Label(
        window, 
        text="To get the attendance report in your mail, Please verify it.", 
        background="grey", 
        foreground="white",
        font=("Arial", 12) 
    )
    button_verify.tooltip.place(
        x=window.winfo_pointerx() + 20, 
        y=window.winfo_pointery() + 20
    )
def show_tooltip2(event):
    button_register.tooltip2 = tk.Label(
        window, 
        text="Register with limited functionalities.", 
        background="grey", 
        foreground="white",
        font=("Arial", 12) 
    )
    button_register.tooltip2.place(
        x=window.winfo_pointerx() + 20, 
        y=window.winfo_pointery() + 20
    )

def hide_tooltip(event):
    button_verify.tooltip.destroy()
    

def hide_tooltip2(event):
    button_register.tooltip2.destroy()


label_title.grid(row=0, column=0, columnspan=2,padx=(40, 0), pady=20)

label_first_name.grid(row=1, column=0, padx=10, pady=10, sticky="E")
entry_first_name.grid(row=1, column=1, padx=10, pady=10, sticky="W")

label_last_name.grid(row=2, column=0, padx=10, pady=10, sticky="E")
entry_last_name.grid(row=2, column=1, padx=10, pady=10, sticky="W")

label_email.grid(row=3, column=0, padx=10, pady=10, sticky="E")
entry_email.grid(row=3, column=1, padx=10, pady=10, sticky="W")

label_password.grid(row=4, column=0, padx=10, pady=10, sticky="E")
entry_password.grid(row=4, column=1, padx=10, pady=10, sticky="W")

label_re_password.grid(row=5, column=0, padx=10, pady=10, sticky="E")
entry_re_password.grid(row=5, column=1, padx=10, pady=10, sticky="W")

button_verify.grid(row=6, column=1, padx=(1,10), pady=20, sticky="E")

register_label.grid(row=7, column=1, padx=(20, 10),columnspan=2, pady=20)

register_label.bind("<Button-1>", lambda event: open_login())

button_verify.bind("<Enter>", show_tooltip)
button_verify.bind("<Leave>", hide_tooltip)

button_register.bind("<Enter>", show_tooltip2)
button_register.bind("<Leave>", hide_tooltip2)

footer_label = tk.Label(window, text="Developed by Tanushree Sarkar & Gopal Sarkar.", font=("Helvetica", 10), bg="#f1f1f1")

# Position the footer label at the bottom of the window
footer_label.pack(side="bottom", fill="x", padx=10, pady=10)
frame.pack()

# run main loop
window.mainloop()
