import smtplib, ssl
from src.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_SENDER

# Create a secure SSL context
context = ssl.create_default_context()


def send_email(recipient: str):
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        login_status = server.login(SMTP_USER, SMTP_PASSWORD)
        if not login_status:
            print("Error logging in SMTP")
            return
        message = f"""
        Welcome to vodahostings, 
        
        Please log into the panel https://panel.vodahostings.com
        
        with these credentials: 
        Username : {recipient}
        Password : Account123!
        
        Enjoy playing!

"""
        server.sendmail(SMTP_SENDER, recipient, message )