# Jesse Zamazanuk
# mailsend.py
# This script sends an email to the specified email address alerting them
# that a leak is present at the specified node
# usage: mailsend.py "Destination email" nodeid or import mailsend to use func
import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def sendLeakAlertEmail(email, node):
    user = 'localizedleakdetector@gmail.com'
    pwd = 'leakdetectpwd'
    sent_from = user
    to = email
    msg = MIMEMultipart()
    msg['From'] = sent_from
    msg['To'] = to
    msg['Subject'] = "Leak Detected"
    body = "A leak has been detected at the node with the following ID: " + str(node)
    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(user,pwd)
        s.sendmail(user,to,text)
        s.quit()
    except:
        print 'Email could not be sent'
