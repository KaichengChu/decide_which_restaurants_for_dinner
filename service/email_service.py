import smtplib
from email.mime.text import MIMEText
from config import CONFIG
import logging
import os
logging.basicConfig(filename="data.log", level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s', filemode='a')

EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(body, to_address="kc081403@ucla.edu"):
    sender_email = CONFIG['email']['sender_email']
    sender_password = EMAIL_PASSWORD
    if not sender_password:
        logging.error("Email password not set in environment variables")
        return {"code": 500, "message": "Email password not set"}
    reciver_email = to_address
    subject = "Daily Restaurant Recommendation"
    if body:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = reciver_email

        "Port 587 is the modern standard and is preferred because it is more flexible, "
        "and port 465 is older but still supported by many services for its direct, encrypted connection."
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, reciver_email, msg.as_string())
            print("Email sent successfully.")
        except Exception as e:
            logging.error("Failed to send email", exc_info=True)
            return {"code": 500, "message": "Failed to send email"}
    else:
        logging.error("No content to send in the email")
        return {"code": 400, "message": "No content to send in the email"}
    return {"code": 200, "message": "Email sent successfully"}
    
