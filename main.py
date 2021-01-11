import requests
from datetime import datetime
import smtplib
import time

My_email = "pythonprojecthowemailworks@gmail.com"
My_password = "Test@12345"

#get your own lat and long from latlong.net
latitude = 22.804565
longitude = 86.202873

# iss position check
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # my position within +5 or -5 deg of thw iss position
    if latitude-5 <= iss_latitude <= latitude+5 <= iss_longitude and longitude-5 <= iss_longitude <= longitude+5:
        return True
    else:
        return False


# sunrise sunset...check if it is night time
def is_night():

    parameters = {
        "lat": latitude,
        "lng": longitude,
        "formatted": 0
    }
    respond = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    data = respond.json()

    sunrise_info = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_info = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if time_now >= sunset_info or time_now <=sunrise_info:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(My_email, My_password)
        connection.sendmail(
            from_addr=My_email,
            to_addrs=My_email,
            msg="Subject:Look Up!\n\n The ISS is above the sky"
    
        )



