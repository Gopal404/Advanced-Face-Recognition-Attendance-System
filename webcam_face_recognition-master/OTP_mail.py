import os
import base64
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
import regis

print(regis.email)
# Create email message
message = Mail(
    from_email='myselfgopalsarkar@outlook.com',
    # to_emails=recipients,
    to_emails='myselfgopalsarkar@gmail.com',
    subject='OTP For Email Verification',
    html_content='<p>Dear User, Use OTP :</p>'+regis.email )

# Send email
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)
