import smtplib
from email.message import EmailMessage
import os

def sendMail(userEmail, token):
    msg= EmailMessage()
    msg["Subject"] = "Verification Email"
    msg["From"] = os.getenv("MY_EMAIL")
    msg["To"] = userEmail
    link = f"http://localhost:5000/api/users/verify/{token}"
    msg.set_content(f"Click on the link to verify your account: {link}")
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("MY_EMAIL"), os.getenv("MY_EMAILPASS"))
            smtp.send_message(msg=msg)
        
        # print("Email sent")
        return True
    except Exception as e:
        print(f"error in sending mail: {e}")
        return False