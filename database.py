import mysql.connector
import requests
import json
from datetime import datetime

url='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=28c31a8964f03149402ab48b7cd02cc9079481f7'

json_dataset = requests.get(url).text

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
    #print(i)
    StationNumber = i['number']
    StationName = i['name']
    AvailableBikeStands = i['available_bike_stands']
    AvailableBikes =  i['available_bikes']
    Unix = i['last_update'] #unix timestamp
    Unix = Unix/1000
    Unix = datetime.fromtimestamp(Unix)
    Date = Unix.date()
    Time = Unix.time()
    # print('Address: ', i['address '])
    # print('Position: ')
    # print('Latitude: ', i['position']['lat'])
    # print('Longitude: ', i['position']['lng'])
    # print('Banking: ', i['banking'])
    # print('Bonus: ', i['bonus'])
    # print('Bike Stands: ', i['bike_stands'])

    print(StationNumber, StationName, AvailableBikes, AvailableBikeStands, Date, Time)


    sql = "INSERT INTO DynamicData (StationNumber, StationName, AvailableBikes, AvailableBikeStands, Date, Time ) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (StationNumber, StationName, AvailableBikes, AvailableBikeStands, Date, Time)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

mydb.close()

