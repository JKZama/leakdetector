# Jesse Zamazanuk
# mailsend.py
# This script sends an email to the specified email address alerting them
# that a leak is present at the specified node
# usage: mailsend.py "Destination email" nodeid or import mailsend to use func
import smtplib
import sys

def sendLeakAlertEmail(email, node):
    user = 'localizedleakdetector@gmail.com'
    pwd = 'leakdetectpwd'
    sent_from = user
    to = email
    subject = 'LeakTest'
    body = 'A leak has been detected at the following Node ID: '+str(node)
    email_body = """\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (sent_from, to, subject, body)

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(user,pwd)
        s.sendmail(user,to,email_body)
        s.quit()
        print 'Email sent!'
    except:
        print 'Email could not be sent'
sendto = str(sys.argv[1]) if len(sys.argv) > 1 else "localizedleakdetector@gmail.com"
n = str(sys.argv[2]) if len(sys.argv) > 1 else "Node ID Error"
sendLeakAlertEmail(sendto,n)
