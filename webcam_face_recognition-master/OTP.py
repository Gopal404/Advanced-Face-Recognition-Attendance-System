import random
import tkinter as tk
from tkinter import messagebox
import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment

email = sys.argv[1]
first_name=sys.argv[2]
last_name=sys.argv[3]


# # Get the value of the email argument
# email = sys.argv[1]
# # Print the value of the email variable
# print("The email address is:", email)

def verify():
    # Generate a random 6-digit number
    otp = random.randint(100000, 999999)
    if(email==''):
        print("Invalid Mail")
        return
    message = Mail(
        from_email='myselfgopalsarkar@outlook.com',
        # to_emails=recipients,
        to_emails=email,
        subject='OTP For Email Verification',
        html_content='<p>Dear '+first_name+' '+last_name+' , Use OTP :</p>'+ str(otp))

    # Send email
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
    
    # Create a tkinter window with a text box and an OK button
    window = tk.Tk()
    window.title("OTP Verification")
    window.geometry("300x200")

    font_style = ("Arial", 12, "bold")
    button_style = {"foreground": "white",
                "background": "green",
                "activeforeground": "red",
                "activebackground": "blue",
                "font": font_style,
                "width": 8,
                "height": 1,
                "cursor": "hand2"}
    
    label = tk.Label(window, text=f"Enter the OTP:")
    label.pack()
    
    entry = tk.Entry(window, width=30, font=font_style)
    entry.pack()

    button = tk.Button(window, text="Verify Mail", command=lambda: check(entry.get(), otp, window), **button_style)
    button.pack()
    window.mainloop()

        # Create email message


def check(user_input, otp, window):
    # Check if the user entered the correct OTP
    if user_input == str(otp):
        messagebox.showinfo("Verification", "Email Varified")
        window.destroy()
        
    else:
        messagebox.showerror("Verification", "Invalid OTP")
verify()
