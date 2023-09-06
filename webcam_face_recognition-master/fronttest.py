############################################# IMPORTING ################################################
from functools import partial
import tkinter as tk
from tkinter import messagebox as mess
from tkinter.font import Font
import cv2,os
import os,sys
import csv
from tkinter import filedialog
from matplotlib import pyplot as plt
import numpy as np
import datetime as dt
from PIL import Image
import pandas as pd
import datetime
import time
import email.utils as eut
from tkinter import*
from tkinter import scrolledtext
import tkinter.scrolledtext as st
from PIL import Image,ImageTk
from datetime import date
import sys
from tkinter import messagebox
import re
import seaborn as sns
from PIL import Image
import pyttsx3



d1 = date.today().strftime("%d-%m-%Y")
label_font = ("Helvetica", 24, "bold")



# retrieve the variable value from the command-line argument
name = sys.argv[1]
# name="Guest"
email=sys.argv[2]
# email="example@example.com"

# use the variable value in your code
# print(f"The variable value is: {name}")

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def count_total():
    res=0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                res = res + 1
        res = res-1
        csvFile1.close()
    else:
        res = 0
    return res
##################################################################################
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

################################### CLEAR BUTTON ###################################################

def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    txt3.delete(0, 'end')
    res = "Take Image for new entry and save profile"
    message1.configure(text=res)
    
###################################################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()
    
############################### CAPTURE IMAGE AND SAVE NEW RECORD IN CSV FILE ########################################################

def Capture_image():
    check_haarcascadefile()
    column= ['SERIAL NO.', 'ID', 'NAME', 'Email']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")

    # check if roll number already exists in CSV file
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r', newline="") as csvFile1:
            reader1 = csv.reader(csvFile1)
            for row in reader1:
                if row[1] == txt.get():
                    messagebox.showerror("Error", "Roll number already exists")
                    return
        csvFile1.close()
    
    # Input validation - check if any field is empty
    if txt.get() == "" or txt2.get() == "" or txt3.get() == "":
        messagebox.showerror("Error", "Please fill all the fields")
        return
        
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r',newline="") as csvFile1:
            reader1 = csv.reader(csvFile1)
            next(reader1) # Skip the first row
            for i in reader1:
                serial = int(i[0]) + 1 # Assuming that the serial number is in the first column of the CSV file
            csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+',newline="") as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(column)
            serial = 1
        csvFile1.close()

    csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    email = (txt3.get())
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                if len(faces) == 1:
                    x, y, w, h = faces[0]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    
                    # display message indicating number of photos taken
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, 'Photo captured ({}/{})'.format(sampleNum, 100), (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                 
                                      
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break

            cam.release()
            cv2.destroyAllWindows()
            res = "Images Taken for ID : " + Id
            row = [serial,Id, name,email]
            row1=[serial,Id, name,email]
            with open('StudentDetails\StudentDetails.csv', 'a+',newline="") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message1.configure(text=res)
            
        else:
            if (name.isalpha() == False):
                messagebox.showerror("Error", "Please Enter Correct Name")
                return
                
    else:
        messagebox.showerror("Error", "Please Enter Valid Email")
        return

############################### SAVE NEW RECORD IN CSV FILE ########################################################

def Save_Record():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    z=count_total()
    message.configure(text='Total Registrations till now  : '+str(z))
    clear()
    messagebox.showinfo("Success", "New Student Added")

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids  
##################################### MARKED ATTENDANCE THROUGH WEBCAM ######################################################

def add_new_admin():
    os.system('python regis.py')
###########################################################################################
def voice(sname,state):
    # Initialize the engine
    engine = pyttsx3.init()

    # Set the voice property to a female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    # Convert text to speech
    text = sname+",has checked "+state
    engine.say(text)
    engine.runAndWait()


def attendance():
    a=pd.read_csv('G:\Final project\webcam_face_recognition-master\webcam_face_recognition-master\StudentDetails\StudentDetails.csv')
    pd.options.mode.chained_assignment = None #For Omitting Warning
    check_haarcascadefile()
    assure_path_exists("StudentDetails/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    c_in=0
    c_out=0
    temp=''
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        ID = 'Unknown'
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                print(ID)
                               
                if temp!=str(ID) and temp!='Unknown':
                    c_in=0
                    c_out=0
            else:
                Id = 'Unknown'
                bb = str(Id)
            temp=str(ID)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
        today = dt.datetime.today().strftime('%d-%m-%Y')
        now = dt.datetime.now().strftime('%H:%M:%S')


        #For Checking In
        if today+'_IN' not in a.columns:
            a[today+'_IN'] = ''
        for i in range(len(a)):
            st=str(a['ID'][i])
            print(len(str(a[today+'_IN'][i]))) 
            if st==str(ID) and (len(str(a[today+'_IN'][i])) == 0 or len(str(a[today+'_IN'][i])) == 3) :
                a[today+'_IN'][i] = now    
                c_in+=1
                if c_in==1:
                    sname=str(a['NAME'][i])
                    voice(sname,'in') 
                    # os.system('python voice.py "{}" "{}"'.format(str(a['NAME'][i]),'in')) 
                
               
        #For Checking Out  
        if today+'_OUT' not in a.columns:
            a[today+'_OUT'] = ''     
        for i in range(len(a)):
            st=str(a['ID'][i])
            print(len(str(a[today+'_OUT'][i])))
            if st==str(ID) and a[today+'_IN'][i]!=now and len(str(a[today+'_IN'][i]))!=0: 
                a[today+'_OUT'][i] = now
                c_out+=1
                if c_out==1:
                    sname=str(a['NAME'][i])
                    voice(sname,'out') 
                #    os.system('python voice.py "{}" "{}"'.format(str(a['NAME'][i]),'out'))                                                                  
    a.to_csv('G:\Final project\webcam_face_recognition-master\webcam_face_recognition-master\StudentDetails\StudentDetails.csv',index=False)
    
    cam.release()
    cv2.destroyAllWindows()
    
            
######################################## DATE ############################################
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## FRONT-END ###########################################

window = tk.Tk()
window.geometry("1530x790+0+0")
window.state('zoomed')
window.resizable(True,False)
window.title("Attendance System")
#bg image
from PIL import Image, ImageTk

# Load the image
img = Image.open(r"G:\Final project\webcam_face_recognition-master\webcam_face_recognition-master\Pictures\tt.jpg")
# Resize the image using Resampling.LANCZOS
img3 = img.resize((1530, 710), resample=Image.Resampling.LANCZOS)
# Convert the Image object into a PhotoImage object
photo = ImageTk.PhotoImage(img3)
# Display the PhotoImage object in a tkinter Label widget
label = tk.Label(window, image=photo)

frame1 = tk.Frame(window, bg="#a1d9d8", borderwidth=1, highlightthickness=1, highlightbackground="gray",bd=1, relief="solid")
frame1.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.15)


frame1.place(relx=0.11, rely=0.17, relwidth=0.37, relheight=0.80)

frame2 = tk.Frame(window, bg="#00bfff",borderwidth=1, highlightthickness=1, highlightbackground="gray",bd=1, relief="solid")
frame2.place(relx=0.51, rely=0.17, relwidth=0.40, relheight=0.80)

robotic_font = Font(family="Robotic Cyborg", size=30, weight="bold")

# Use the custom font for the message label
message3 = tk.Label(window, text="Automated Facial Recognition Attendance", bg="#0077be", fg="white", width=70, font=robotic_font, padx=5, pady=5,bd=1, relief="solid")
message3.pack(fill=tk.X)
label.pack()


n1 = tk.Label(window, text="Welcome "+name, bg="#0077be", fg="white", width=25, height=1, font=('Gill Sans', 14))
n1.place(x=147, y=85)


frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.81, rely=0.12, relwidth=0.10, relheight=0.04)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.69, rely=0.12, relwidth=0.12, relheight=0.04)

datef = tk.Label(frame4, text="   "+day+"-"+mont[month]+"-"+year+"    ", fg="white", bg="#0077be", width=35, height=1, font=('Gill Sans', 16, 'bold'))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="white", bg="#0077be", width=35, height=1, font=('Gill Sans', 16, 'bold'))
clock.pack(fill='both', expand=1)



tick()

head2 = tk.Label(frame2, text="Manage Students Registration", fg="black",bg="#00aeff" ,font=('Gill Sans', 17, ' bold '),bd=1 ,relief=tk.SOLID)
head2.pack(fill=tk.X, padx=10, pady=13)

head1 = tk.Label(frame1, text="Manage Students Attendance", fg="black", bg="#00aeff", font=('Gill Sans', 17, 'bold'),bd=1,relief=tk.SOLID)
head1.pack(fill=tk.X, padx=10, pady=13)


lbl = tk.Label(frame2, text="Enter Roll No.",width=20  ,height=1  ,fg="black"  ,bg="#00bfff" ,font=('Gill Sans', 17) )
lbl.place(x=120, y=50)

txt = tk.Entry(frame2, width=30, fg="black", bg="white", font=('Gill Sans', 16), bd=1, relief=tk.SOLID)
txt.place(x=80, y=82)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="#00bfff" ,font=('Gill Sans', 17))
lbl2.place(x=120, y=130)

txt2 = tk.Entry(frame2,width=30 ,fg="black",bg="white",font=('Gill Sans', 16),bd=1, relief=tk.SOLID)
txt2.place(x=80, y=163)

lbl3 = tk.Label(frame2, text="Enter Email",width=20  ,fg="black"  ,bg="#00bfff" ,font=('Gill Sans', 17))
lbl3.place(x=120, y=211)

txt3 = tk.Entry(frame2,width=30 ,fg="black",bg="white",font=('Gill Sans', 16),bd=1, relief=tk.SOLID)
txt3.place(x=80, y=244)

message1 = tk.Label(frame2, text="Before Saving, Please Capture Image" ,bg="#00bfff" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('Gill Sans', 15))
message1.place(x=40, y=300)

message = tk.Label(frame2, text="" ,bg="#BCBCEE" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('Gill Sans', 16))
message.place(x=7, y=495)


lbl3 = tk.Label(frame1, text="Take & View Attendance",width=20  ,fg="black"  ,bg="#a1d9d8"  ,height=1 ,font=('Gill Sans', 16))
lbl3.place(x=128, y=167)


res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = res-1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now: '+str(res), bg='#00bfff')

####################### VIEW STUDENTS RECORD ################################

def delete_student(report_box, header, data, row_num,report_window):
    # Get the selected data from the data list
    selected_data = data[row_num]

    # Confirm the deletion with a popup message box
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the record of {selected_data[1]}?")

    if confirm:
        # Open the CSV file in write mode
        with open('StudentDetails/StudentDetails.csv', 'w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the header row to the CSV file
            writer.writerow(header)

            # Write all the rows except the selected row to the CSV file
            for i, row in enumerate(data):
                if i != row_num:
                    writer.writerow(row)

        # Remove the selected row from the data list
        data.pop(row_num)

        # Remove the selected row from the report box
        report_box.delete(f"{row_num+1}.0", f"{row_num+1}.end")

        # Show a popup message to confirm the deletion
        messagebox.showinfo("Record Deleted", "Record deleted successfully!")
        report_window.destroy()
        z=count_total()
        message.configure(text='Total Registrations till now  : '+str(z))
        students_record()
import csv
def update_student(student_id, report_window):
    print(student_id)
    # Open the CSV file and create a CSV reader object
    with open('StudentDetails/StudentDetails.csv', 'r') as file:
        reader = csv.reader(file)

        # Extract the header row
        header = next(reader)

        # Initialize a list to hold the data
        data = []

        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row to the data list
            data.append(row)
        # check if roll number already exists in CSV file

    # Find the row with the matching student ID
    for i, row in enumerate(data):
        if row[1] == student_id:
            # Create a new window for updating details
            # Create the Toplevel window
            update_window = tk.Toplevel()

            # Set the window size
            update_window.geometry("320x470")
            update_window.title("Update Informations")


            # Create labels and entry fields for each column
            label_font = ('Arial', 16)
            entry_font = ('Helvetica', 13)

            # tk.Label(update_window, text="ID", font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            # roll_no_entry = tk.Entry(update_window, font=entry_font)
            # roll_no_entry.insert(0, row[0])
            # roll_no_entry.config(state="disabled")
            # roll_no_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

            tk.Label(update_window, text="Roll No:", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            name_entry = tk.Entry(update_window, font=entry_font, readonlybackground="white")
            name_entry.insert(0, row[1])
            name_entry.config(state="disabled")
            name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            tk.Label(update_window, text="Name:", font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            email_entry = tk.Entry(update_window, font=entry_font)
            email_entry.insert(0, row[2])
            email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

            tk.Label(update_window, text="Email:", font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            phone_entry = tk.Entry(update_window, font=entry_font)
            phone_entry.insert(0, row[3])
            phone_entry.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

            # Create a button to update the details
            def update_details():
                # if exists:
                #     with open("StudentDetails\StudentDetails.csv", 'r', newline="") as csvFile1:
                #         reader1 = csv.reader(csvFile1)
                #         for row in reader1:
                #             if row[1] == name_entry.get() :
                #                 messagebox.showerror("Error", "Roll number already exists")
                #                 return
                #     csvFile1.close()

                updated_row = row.copy()
                updated_row[1] = name_entry.get() if name_entry.get() else updated_row[1]
                updated_row[2] = email_entry.get() if email_entry.get() else updated_row[2]
                updated_row[3] = phone_entry.get() if phone_entry.get() else updated_row[3]

                data[i] = updated_row

                with open('StudentDetails/StudentDetails.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(data)

                messagebox.showinfo("Success", "Student details updated successfully!")
                update_window.destroy()
                report_window.destroy()
                students_record()

            button_width = 15
            button_height = 2
            button_font = ('Helvetica', 12)
            tk.Button(update_window, text="Update", command=update_details, cursor="hand2", width=button_width, height=button_height, bg="green", fg="white", font=button_font).grid(row=4, column=0, columnspan=2)
            # tk.Label(update_window, text="ID", font=label_font).grid(row=0, column=0, padx=20, pady=20, sticky="nsew") 
            break

def students_record():
    # Open the CSV file
    with open('StudentDetails/StudentDetails.csv', 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Extract the header row
        header = next(reader)

        # Initialize a list to hold the data
        data = []

        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row to the data list
            data.append(row)

    # Create a new window to show the report
    report_window = tk.Toplevel(window)
    report_window.geometry("900x600")
    report_window.state('zoomed')
    report_window.title("Students Record")
    report_window.configure(bg="#3b3f42")
    
    heading_label = tk.Label(report_window, text="Students Record", font=("Arial", 28), bg="#3b3f42",fg="Orange", padx=5, pady=5)
    heading_label.pack(fill="x")
    
    
    # Add a scrolled text widget to the window
    report_box = st.ScrolledText(report_window, width=100, height=30, pady=5, font=("Arial", 16))
    report_box.pack(pady=(5, 0))  # add 20 pixels of padding on top
    report_box.tag_configure("header", background="blue", foreground="white")

    # Display the header in the scrolled text widget
    report_box.insert(tk.INSERT, "{:<35} {:<40} {:<55} {:<20}\n".format( "Roll No.", header[2], header[3], "Actions"), "header")

    
    # Display the report data in the scrolled text widget
    for i, row in enumerate(data):
        # Add a label to display the data
        report_box.insert(tk.INSERT, " {:<22}"    " {:<35}"   " {:<50}""".format( row[1], row[2], row[3]))

        # Add an update button for each row
        # Add an update button for each row
        update_button = tk.Button(report_box, text="Update", font=("Arial", 12), bg='#5bcdfa', cursor='hand2', borderwidth=0, bd=1, padx=2, pady=2)
        update_button.configure(command=lambda roll_num=row[1]: update_student(roll_num, report_window))


        report_box.window_create(tk.INSERT, window=update_button)

        report_box.window_create(tk.INSERT, window=update_button)
        report_box.insert(tk.INSERT, "   ")  # Add some spacing after the update button

        # Add a delete button for each row
        delete_button = tk.Button(
            report_box,
            text="Delete",
            font=("Arial", 12),
            command=lambda row_num=i: delete_student(report_box, header, data, row_num, report_window),
            bg="#ff0040",
            cursor="hand2",
            borderwidth=0,
            bd=1,
            padx=2,
            pady=2,
        )
        report_box.window_create(tk.INSERT, window=delete_button)



        # Add a newline character after each row
        report_box.insert(tk.INSERT, "\n")

        # Configure the font of the data and buttons
        report_box.tag_configure("data", font=("Arial", 15))
        report_box.tag_configure("button", font=("Arial", 12))

        # Apply the "data" tag to the data label
        report_box.tag_add("data", f"{i+2}.0", f"{i+2}.end")

        # Apply the "button" tag to the update and delete buttons
        report_box.tag_add("button", f"{i+2}.end-2c", f"{i+2}.end")
        report_box.tag_add("button", f"{i+2}.end-7c", f"{i+2}.end-5c")


    # Configure the report box to be read-only
    report_box.configure(state=tk.DISABLED)


################################ VIEW ATTENDANCE ###########################################################
def attendance_by_date():
    # Create a new window
    date_window = tk.Toplevel(window)
    date_window.state('zoomed')
    date_window.title("Attendance Details By Date")
    date_window.configure(bg="#3b3f42")
    
    heading_label = tk.Label(date_window, text="Attendance Record", font=("Arial", 16), bg="lightblue", padx=10, pady=7)
    heading_label.pack(fill="x")

    # Add a label and a dropdown menu for selecting the date
    date_label = tk.Label(date_window, text="Select Date:",bg="#3b3f42", fg="white",pady=5,width=20  ,height=1,font=('Gill Sans', 15))
    date_label.pack()

    # Create three StringVars to store the selected day, month, and year
    day_var = tk.StringVar(date_window, value='01')
    month_var = tk.StringVar(date_window, value='01')
    year_var = tk.StringVar(date_window, value='2023')

    # Create three OptionMenus for day, month, and year
    day_menu = tk.OptionMenu(date_window, day_var, *range(1, 32))
    month_menu = tk.OptionMenu(date_window, month_var, *range(1, 13))
    year_menu = tk.OptionMenu(date_window, year_var, *range(2021, 2040))

    

    # Pack the OptionMenus
    day_menu.place(x=570, y=90)
    month_menu.place(x=650, y=90)
    year_menu.place(x=730, y=90)

    # Add a function to get the selected date
    def get_date():
        # Retrieve the selected day, month, and year
        day = day_var.get()
        month = month_var.get()
        year = year_var.get()

        # Combine the day, month, and year into a date string
        date_str = f"{day}-{month}-{year}"
        return date_str

    # Add a scrolledtext widget to display the attendance records
    records_text = scrolledtext.ScrolledText(date_window, height=27, width=115)
    records_text.pack(pady=70)
    records_text.configure(bg='#CACAFF')
    
    def show_attendance():
        clear_attendance()
        # Retrieve the selected date
        date_str = get_date()
        
        # Convert the date string to a datetime object
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
        formatted_date = date.strftime('%d-%m-%Y')

        # Search the attendance records for the given date
        with open('StudentDetails/StudentDetails.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader) # skip the header row
            date_index = header.index(formatted_date+'_IN') if formatted_date+'_IN' in header else -1
            date_index2 = header.index(formatted_date+'_OUT') if formatted_date+'_OUT' in header else -1
            if date_index == -1:
                messagebox.showinfo("No Records Found", "No Records Found For The Given Date.")
            else:
                records_text.insert(tk.END, "Attendance Records For: " + date_str  + ":\n")
                header = f"{'ID':<25}{'NAME':<20}{'CHECK-IN':<10}{'CHECK-OUT':<12}{'SPENT TIME':<20}\n"
                # Insert the header string with a blue background and bold font
                records_text.tag_config('header', background='blue', foreground='white')
                records_text.insert(tk.END, header, 'header')

                attendance_data = []
                for row in reader:
                    if row[date_index]!='' and row[date_index2]!='':
                        time_in = datetime.datetime.strptime(row[date_index], '%H:%M:%S')
                        time_out = datetime.datetime.strptime(row[date_index+1], '%H:%M:%S')
                        time_diff = time_out - time_in
                        time_diff_str = str(time_diff)
                        records_text.insert(tk.END, f"{row[1]:<20} {row[2]:<23} {row[date_index]:<10} {row[date_index+1]:<12} {time_diff_str:<20}\n")
                        attendance_data.append([row[1], row[2], row[date_index], row[date_index+1], time_diff_str])

    def show_graph():
        # Clear the records_text widget
        records_text.delete('1.0', tk.END)

        # Retrieve the selected date
        date_str = get_date()

        # Convert the date string to a datetime object
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
        formatted_date = date.strftime('%d-%m-%Y')

        # Search the attendance records for the given date
        with open('StudentDetails/StudentDetails.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader) # skip the header row
            date_index = header.index(formatted_date+'_IN') if formatted_date+'_IN' in header else -1
            date_index2 = header.index(formatted_date+'_OUT') if formatted_date+'_OUT' in header else -1
            if date_index == -1:
                messagebox.showinfo("No Records Found", "No Records Found For The Given Date.")
            else:
                records_text.insert(tk.END, "Attendance Records For: " + date_str  + ":\n")
                header = f"{'ID':<25}{'NAME':<20}{'CHECK-IN':<10}{'CHECK-OUT':<12}{'SPENT TIME':<20}\n"
                # Insert the header string with a blue background and bold font
                records_text.tag_config('header', background='blue', foreground='white')
                records_text.insert(tk.END, header, 'header')
                attendance_data = []
                names = []
                times = []
                colors = plt.cm.Set2(range(len(header)))
                for row in reader:
                    if row[date_index]!='' and row[date_index2]!='':
                        time_in = datetime.datetime.strptime(row[date_index], '%H:%M:%S')
                        time_out = datetime.datetime.strptime(row[date_index2], '%H:%M:%S')
                        time_diff = time_out - time_in
                        minutes, seconds = divmod(time_diff.seconds, 60)
                        time_diff_str = f"{minutes:02d}:{seconds:02d}"
                        records_text.insert(tk.END, f"{row[1]:<20} {row[2]:<23} {row[date_index]:<10} {row[date_index+1]:<12} {time_diff_str:<20}\n")
                        attendance_data.append([row[1], row[2], row[date_index], row[date_index2], time_diff_str])
                        names.append(row[2])
                        times.append(time_diff.seconds / 60.0)
                # Sort the names and times in descending order based on times
                names, times = zip(*sorted(zip(names, times), key=lambda x: x[1], reverse=True))

                # Define the color palette
                colors = sns.color_palette('pastel')

                # Set the seaborn style
                sns.set_style('whitegrid')

                # Create the bar graph and line graph
                fig, ax1 = plt.subplots(figsize=(14, 6))

                ax1.bar(names, times, color=colors[:len(names)], width=0.5)
                ax1.plot(names, times, color='gray', linewidth=2, marker='o')

                # Set the axis labels for both graphs
                ax1.set_xlabel('Name of Students', fontsize=16, fontweight='bold', labelpad=10)
                ax1.set_ylabel('Time Spent (Minutes)', fontsize=16, fontweight='bold', labelpad=10)

                # Define the date string and set the title
                fig.suptitle("Attendance record for " + date_str, fontsize=24, fontweight='bold')

                # Rotate the x-axis labels for bar and line graph
                ax1.set_xticklabels(names, rotation=45, ha='right')

                # Format the y-axis ticks as minutes and seconds for both graphs
                def format_y_tick(tick_value, tick_number):
                    minutes, seconds = divmod(int(tick_value), 60)
                    return f"{minutes:02d}:{seconds:02d}"

                ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_y_tick))

                # Calculate the total present students and total time spent
                total_present = len(names)
            
                # Add a text box at the top right corner of the plot
                ax1.text(0.95, 0.95, f"Total Present Students: {total_present}",
                        transform=ax1.transAxes,
                        ha='right', va='top',
                        fontsize=16,
                        bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

                # Add time spent values above each bar for both graphs
                for i, v in enumerate(times):
                    ax1.text(i, v + 1, f"{int(v):d}:{int((v-int(v))*60):02d}"+" min", ha='center', va='bottom', fontsize=10)

                # Customize the plot layout for both graphs
                sns.despine()
                ax1.tick_params(axis='both', which='both', length=0)
                plt.subplots_adjust(wspace=0.4, left=0.1, right=0.9, bottom=0.2, top=0.8)

                # Maximize the window
                mng = plt.get_current_fig_manager()
                mng.window.state('zoomed')

                # Display the graph
                plt.show()


    def clear_attendance():
        # Clear the contents of the records_text widget
        records_text.delete('1.0', tk.END) 

    #For exporting attendance report
    def export_report():
        # Retrieve the selected date
        date_str = get_date()        
        # Convert the date string to a datetime object
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
        formatted_date = date.strftime('%d-%m-%Y')
        # Search the attendance records for the given date
        with open('StudentDetails/StudentDetails.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader) # skip the header row
            date_index = header.index(formatted_date+'_IN') if formatted_date+'_IN' in header else -1
            date_index2 = header.index(formatted_date+'_OUT') if formatted_date+'_OUT' in header else -1
            if date_index == -1:
                records_text.insert(tk.END, "No Records Found For The Given Date.")
            else:
                attendance_data = []
                for row in reader:
                    if row[date_index]!='' and row[date_index2]!='':
                        time_in = datetime.datetime.strptime(row[date_index], '%H:%M:%S')
                        time_out = datetime.datetime.strptime(row[date_index+1], '%H:%M:%S')
                        time_diff = time_out - time_in
                        time_diff_str = str(time_diff)
                        attendance_data.append([row[1], row[2], row[date_index], row[date_index+1], time_diff_str])
        # Use file dialog to select output directory
        output_dir = filedialog.askdirectory(title="Select output directory")
        if output_dir:
            output_path = f"{output_dir}/Attendance_{formatted_date}.csv"
            with open(output_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Name', 'Time In', 'Time Out', 'Spent Time'])
                for row in attendance_data:
                    writer.writerow(row)
            messagebox.showinfo("Success", "Report exported successfully.")

    #For mailing attendance report      
    def mail_report():
        # Retrieve the selected date
        date_str = get_date()        
        # Convert the date string to a datetime object
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
        formatted_date = date.strftime('%d-%m-%Y')
        # Search the attendance records for the given date
        with open('StudentDetails/StudentDetails.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader) # skip the header row
            date_index = header.index(formatted_date+'_IN') if formatted_date+'_IN' in header else -1
            date_index2 = header.index(formatted_date+'_OUT') if formatted_date+'_OUT' in header else -1
            if date_index == -1:
                records_text.insert(tk.END, "No Records Found For The Given Date.")
            else:
                attendance_data = []
                for row in reader:
                    if row[date_index]!='' and row[date_index2]!='':
                        time_in = datetime.datetime.strptime(row[date_index], '%H:%M:%S')
                        time_out = datetime.datetime.strptime(row[date_index+1], '%H:%M:%S')
                        time_diff = time_out - time_in
                        time_diff_str = str(time_diff)
                        attendance_data.append([row[1], row[2], row[date_index], row[date_index+1], time_diff_str])

        with open(f'Attendance_{formatted_date}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Time In', 'Time Out', 'Spent Time'])
            for row in attendance_data:
                writer.writerow(row)

        os.system('python mail.py "{}" "{}" "{}"'.format(name,email,formatted_date))
        messagebox.showinfo("Success", "Report mailed successfully.")
    # Add a button to display the attendance records
    show_button = tk.Button(date_window, text="Show Attendance", command=show_attendance, bg="#2196f3", fg="#ffffff",width=18  ,height=1,font=('Gill Sans', 15), borderwidth=0, activebackground="#1e88e5", activeforeground="#ffffff", cursor="hand2")
    show_button.place(x=210, y=600)
    
    show_button = tk.Button(date_window, text="Show Graph", command=show_graph, bg="#7979CD", fg="#ffffff",width=18  ,height=1,font=('Gill Sans', 15), borderwidth=0, activebackground="#1e88e5", activeforeground="#ffffff", cursor="hand2")
    show_button.place(x=455, y=600)

    # clear_button = tk.Button(date_window, text="Clear Attendance", command=clear_attendance,bg="#c190c6", fg="#ffffff",width=14  ,height=1,font=('Gill Sans', 15), borderwidth=0, activebackground="#1e88e5", activeforeground="#ffffff", cursor="hand2")
    # clear_button.place(x=610, y=600)
    
    
    clear_button = tk.Button(date_window, text="Export Report", command=export_report, bg="#8bc34a", fg="#ffffff", width=18, height=1, font=('Gill Sans', 15), borderwidth=0, activebackground="#689f38", activeforeground="#ffffff", cursor="hand2")
    clear_button.place(x=710, y=600)

    
    mail_button = tk.Button(date_window, command=mail_report, text="Mail Report", bg="#00FF00", fg="#ffffff", width=18, height=1, font=('Gill Sans', 15), borderwidth=0, activebackground="#1e88e5", activeforeground="#ffffff", cursor="hand2")
    mail_button.place(x=950, y=600)

###################### BUTTONS ##################################


takeImg = tk.Button(frame2, text="Capture Image", command=Capture_image, fg="white", bg="#0077be", width=15, height=1, activebackground="white", font=('Gill Sans', 15), cursor="hand2", borderwidth=0)
takeImg.place(x=172, y=350)

trainImg = tk.Button(frame2, text="Save Profile", command=Save_Record, fg="white", bg="#009900", width=23, height=1, activebackground="white", font=('Gill Sans', 15), cursor="hand2", borderwidth=0)
trainImg.place(x=127, y=420)

trackImg = tk.Button(frame1, text="Show Students Record", command=students_record, fg="white", bg="#00b300", width=35, height=1, activebackground="white", font=('Gill Sans', 15), cursor="hand2", border=0)

trackImg.place(x=50,y=85)

trackImg = tk.Button(frame1, text="Take Attendance", command=attendance, fg="white", bg="#2050df", width=15, height=1, activebackground="white", font=('Gill Sans', 15), cursor="hand2", borderwidth=0)
trackImg.place(x=50, y=230)

trackImg1 = tk.Button(frame1, text="View Attendance", command=attendance_by_date, fg="white", bg="#2050df", width=15, height=1, activebackground="white", font=('Gill Sans', 15), cursor="hand2", borderwidth=0)
trackImg1.place(x=260, y=230)


newadmin = tk.Button(frame1, text="Add New Admin", command=add_new_admin, fg="white", bg="#354052", width=35, height=1, activebackground="white", font=('Gill Sans', 15), cursor="hand2", borderwidth=0)
newadmin.place(x=50, y=350)


quitWindow = tk.Button(frame1, text="Log Out", command=lambda: confirm_quit(window), fg="white", bg="red", width=35, height=1, activebackground="white", font=('Gill Sans', 15), cursor="hand2", borderwidth=0)
quitWindow.place(x=50, y=450)

def confirm_quit(window):
    answer = messagebox.askquestion("Confirmation", "Are you sure you want to log out?")
    if answer == 'yes':
        window.destroy()
        os.system('python login.py')


##################### END ######################################
window.mainloop()
################################################################