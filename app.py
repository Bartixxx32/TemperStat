import csv
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
from datetime import datetime
from flask import render_template, Flask, request
import Adafruit_DHT
import RPi.GPIO as GPIO

pin = 4
sensor = Adafruit_DHT.DHT11

app = Flask(__name__)

data_temp = []
data_hum = []
data_time = []
last_log_time = time.time()  # Initialize last log time


@app.route('/mail', methods=['POST', 'GET'])
def mail():
    # Email configuration
    SUBJECT = 'IOT Project :: TemperStat Readings'
    FILENAME = 'readings.csv'
    FILEPATH = 'readings.csv'
    MY_EMAIL = 'temperstat@gmail.com'
    MY_PASSWORD = 'temperstat20'
    TO_EMAIL = request.form['email']
    toemail = TO_EMAIL
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    # Compose email
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = COMMASPACE.join([TO_EMAIL])
    msg['Subject'] = SUBJECT
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(FILEPATH, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=FILENAME)
    msg.attach(part)
    
    # Send email
    smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(MY_EMAIL, MY_PASSWORD)
    smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
    smtpObj.quit()
    return render_template("mail.html", toemail=toemail)


@app.route('/', methods=['POST', 'GET'])
def index():
    global last_log_time  # Use the global variable for last log time
    nowtime = datetime.now().strftime("%H:%M:%S")
    temperature, humidity = sensor_1()
    data_temp.append(temperature)
    data_hum.append(humidity)
    data_time.append(nowtime)
    temperature_max = max(data_temp)
    humidity_max = max(data_hum)
    temperature_min = min(data_temp)
    humidity_min = min(data_hum)
    
    # Check if 30 minutes have passed since the last log
    if time.time() - last_log_time >= 1800:  # 30 minutes = 1800 seconds
        # Log data to CSV
        with open('readings.csv', 'a') as file:
            writer = csv.writer(file)
            for i in range(len(data_temp)):
                writer.writerow([data_time[i], data_temp[i], data_hum[i]])
        
        # Reset data lists and update last log time
        data_temp.clear()
        data_hum.clear()
        data_time.clear()
        last_log_time = time.time()
    render_template("index.html", temperature=temperature, humidity=humidity,
                    data_temp=data_temp, data_time=data_time, data_hum=data_hum,
                    temperature_max=temperature_max, humidity_max=humidity_max,
                    temperature_min=temperature_min, humidity_min=humidity_min)
    
    return render_template("index.html", temperature=temperature, humidity=humidity,
                           temperature_max=temperature_max, humidity_max=humidity_max,
                           temperature_min=temperature_min, humidity_min=humidity_min)


def sensor_1():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return temperature, humidity


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
