import smtplib

TO = 'borg.aditya@gmail.com'
SUBJECT = 'TEST MAIL'
TEXT = 'sent from python. created w/ <3 by 4ditya. iot project will be legendary.!'

# Gmail Sign In
gmail_sender = 'temperstat@gmail.com'
gmail_passwd = input()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_sender, gmail_passwd)

BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print ('email sent')
except:
    print ('error sending mail')

server.quit()