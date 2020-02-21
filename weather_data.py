import requests
import json
from datetime import datetime
import mysql.connector

url='https://api.darksky.net/forecast/313018b2afc91b7825d89c2740c19873/53.3498,-6.0'

json_dataset = requests.get(url).text
test = json.loads(json_dataset)

mydb = mysql.connector.connect(
    host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="picanha123",
    database='BikeData'
)

mycursor = mydb.cursor()

Unix = test['currently']['time']
Unix = datetime.fromtimestamp(Unix)
Date = Unix.date()
Time = Unix.time()
Temperature = round((test['currently']['temperature']-32) * 5/9, 1)
Rainfall = test['currently']['precipIntensity']

sql = "INSERT INTO WeatherData (Date, Time, Rainfall, Temperature) VALUES (%s, %s, %s, %s)"
val = (Date, Time, Rainfall, Temperature)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

mydb.close()