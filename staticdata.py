import mysql.connector
import requests
import json


url='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=28c31a8964f03149402ab48b7cd02cc9079481f7'

json_dataset = requests.get(url).text

with open('stations_data.json', 'w') as f:
    json.dump(json_dataset, f)

print(json_dataset)
test = json.loads(json_dataset)

mydb = mysql.connector.connect(
    host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="picanha123",
    database='BikeData'
)

mycursor = mydb.cursor()

for i in test:
    StationNumber = i['number']
    StationName = i['name']
    Address = i['address']
    Latitude = i['position']['lat']
    Longitude = i['position']['lng']
    Banking = i['banking']

    print(StationNumber, StationName, Address, Latitude, Longitude, Banking)

    sql = "INSERT INTO StaticData (StationNumber, StationName, Address, Latitude, Longitude, Banking) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (StationNumber, StationName, Address, Latitude, Longitude, Banking)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

mydb.close()