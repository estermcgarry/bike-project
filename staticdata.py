import mysql.connector
import requests
import json

url='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=API'

json_dataset = requests.get(url).text

print(json_dataset)
test = json.loads(json_dataset)

mydb = mysql.connector.connect(
    host="aws_host_link",
    user="admin",
    passwd="meu_password",
    database='database'
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
