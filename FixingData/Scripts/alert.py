import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    
    user = "MiMaEmailAlerts@gmail.com"
    password = "oekofosgmroxdpbl"
    
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = user


    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

subject = "the file has finished completion"
body = "the file has finished completion"
to = "guillotkaleb01@gmail.com"
email_alert(subject=subject, body=body, to=to)
