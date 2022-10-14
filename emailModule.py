import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class emailModule():
    def sendMail(self, sender, password, reciever, subject, filename=0, body=''):
        msg = MIMEMultipart()
        
        msg['From'] = sender
        msg['To'] = reciever
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))

        if (filename != 0):
            attachment = open(filename, 'rb')

            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename=%s" % filename)
            msg.attach(p)
            attachment.close()
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender, password)
        text = msg.as_string()
        s.sendmail(sender, reciever, text)
        s.quit()
    def argsHelp(self):
        print("The arguments go in in the following order")
        print("Sender, Password, Receiver, Body, Subject, Filename*")
