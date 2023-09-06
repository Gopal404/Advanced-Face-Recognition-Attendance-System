import os
import base64
import sys
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment

name = sys.argv[1]
email=sys.argv[2]
d1=sys.argv[3]

with open('G:/Final project/webcam_face_recognition-master/webcam_face_recognition-master/Attendance'+'_'+d1+'.csv', 'rb') as f:
    file_data = f.read()
file_content = base64.b64encode(file_data).decode()

# Create email message
d1 = date.today().strftime("%d-%m-%Y")
message = Mail(
    from_email='exampler@outlook.com',
    # to_emails=recipients,
    to_emails=email,
    subject='Attendance Report',
    html_content='<p>Dear '+name+', Attendance report for '+d1+'</p>')
attachment = Attachment(
    file_content=file_content,
    file_name='Attendance'+'_'+d1+'.csv',
    file_type='text/csv')
message.attachment = attachment

# Send email
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)
