import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
from datetime import datetime, timedelta
from flask import Flask, render_template, request
import Adafruit_DHT
import RPi.GPIO as GPIO

pin = 4
sensor = Adafruit_DHT.DHT11

app = Flask(__name__)

data_temp = []
data_hum = []
data_time = []
last_log_time = datetime.now()


@app.route('/mail', methods=['POST'])
def mail():
    SUBJECT = 'IOT Project :: TemperStat Readings'
    FILENAME = 'readings.csv'
    FILEPATH = 'readings.csv'
    MY_EMAIL = 'temperstat@gmail.com'
    MY_PASSWORD = 'temperstat20'
    TO_EMAIL = request.form['email']
    toemail = TO_EMAIL
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = COMMASPACE.join([TO_EMAIL])
    msg['Subject'] = SUBJECT
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(FILEPATH, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=FILENAME)
    msg.attach(part)
    smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(MY_EMAIL, MY_PASSWORD)
    smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
    smtpObj.quit()
    return render_template("mail.html", toemail=toemail)


@app.route('/', methods=['GET'])
def index():
    global last_log_time
    temperature, humidity = sensor_1()
    nowtime = datetime.now().strftime("%H:%M:%S")

    data_temp.append(temperature)
    data_hum.append(humidity)
    data_time.append(nowtime)

    if datetime.now() >= last_log_time + timedelta(minutes=30):
        log_data()
        last_log_time = datetime.now()

    temperature_max = max(data_temp)
    humidity_max = max(data_hum)
    temperature_min = min(data_temp)
    humidity_min = min(data_hum)

    return render_template("index.html", temperature=temperature, humidity=humidity, data_temp=data_temp,
                           data_time=data_time, data_hum=data_hum, temperature_max=temperature_max,
                           humidity_max=humidity_max, temperature_min=temperature_min, humidity_min=humidity_min)


def log_data():
    with open('readings.csv', 'a') as file:
        writer = csv.writer(file)
        for i in range(len(data_temp)):
            writer.writerow([data_time[i], data_temp[i], data_hum[i]])
    # Clear data lists after logging
    data_temp.clear()
    data_hum.clear()
    data_time.clear()


def sensor_1():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return temperature, humidity


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
