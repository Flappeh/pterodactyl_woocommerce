import os
import sys
from smtplib import SMTP
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

#Setup SMTP Server
smtp_server = os.getenv('smtp_host')
smtp_user = os.getenv('smtp_username')
smtp_password = os.getenv('smtp_password')
smtp_port = os.getenv('smtp_port')
smtp_from = 'info@infinity-projects.de'
smtp_to = ['akunbuatgta@gmail.com','business.sinar@gmail.com']

def send_email(message_mail, subject, user_email=None):
    try:
        if user_email:
            smtp_to.append(user_email) 
        msg = MIMEText(message_mail,'plain')
        msg['Subject'] = subject
        msg['From'] = smtp_from
        conn = SMTP(host='smtp.ionos.de',port=587)
        conn.set_debuglevel(False)
        conn.login(user=smtp_user,password=smtp_password)
        try:
            conn.sendmail(smtp_from,smtp_to,msg.as_string())
        finally:
            conn.quit()
            print("Email Sent")
    except:
        sys.exit("Fail Sending Mail ")
