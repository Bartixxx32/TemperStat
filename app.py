'''
Copyright (c) Project TemperStat. All rights reserved.
by Aditya Borgaonkar & Sahil Gothoskar, 2020.

https://github.com/adityaborgaonkar
https://github.com/SahilGothoskar

'''
import smtplib
from itertools import chain

readings = [ ['12:45','30 Deg Cel','45 %'],['12:46','32 Deg Cel','51 %'],['12:47','31 Deg Cel','65 %'] ] 
readings = list(chain.from_iterable(readings))
readings = '\n'.join(map(str, readings))

# sgothoskar967@gmail.com
# borg.aditya@gmail.com
TO = 'sgothoskar967@gmail.com'
SUBJECT = 'TemperStat Readings'
TEXT = 'TemperStat\n'+'Time, Temperature & Humidity Readings\n'+readings

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








