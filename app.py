from flask_googlemaps import GoogleMaps
import mysql.connector
from flask import Flask, render_template
import json

app = Flask(__name__,  template_folder="./templates")

app.config['GOOGLEMAPS_KEY'] = "AIzaSyBR7esRJtzTOqcv53Bk3t1xpiCF0YPO-3I"
app.config['WEATHER_KEY'] = "https://api.darksky.net/forecast/313018b2afc91b7825d89c2740c19873/53.3498,-6.0"

# Initialize the extension
GoogleMaps(app)

@app.route('/')
def index():

    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT StationNumber, StationName, Latitude, Longitude FROM StaticData ORDER BY StationName ASC;")

    markers = []
    station_names = []

    for i in mycursor:
        station = {"number": i[0], "name" : i[1], "latitude" : i[2], "longitude" : i[3]}
        markers.append(station)

        # Selecting information to be used in the dropdown menu
        infoDropdown = {"number": i[0], "name" : i[1]}
        station_names.append(infoDropdown)

    mycursor.close()

    weather_cursor = mydb.cursor()
    weather_cursor.execute("SELECT * FROM WeatherData WHERE Date=(SELECT max(Date) FROM WeatherData) ORDER BY Time DESC LIMIT 1;")

    #Store weather info into a dictionary
    weather_info = []
    for i in weather_cursor:
        info = {"Date": i[0], "Time": i[1], "Rainfall": i[2], "Temperature": i[3], "Icon": i[4],"WindSpeed": i[5]}
        weather_info.append(info)
        print(i)
    
    weather_cursor.close()
    mydb.close()

    return render_template('index.html', markers=json.dumps(markers), station_names=json.dumps(station_names), weather_info=json.dumps(weather_info))

@app.route('/station/<station>')
def home(station):
    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )

    mycursor = mydb.cursor()
    mycursor.execute("select StationNumber, StationName, AvailableBikes, AvailableBikeStands from DynamicData where StationNumber = " + station + " order by time desc limit 1;")
    message = "No information"
    for i in mycursor:
        message = "<b>" + i[1] + "</b> <br>Available bikes: " + str(i[2]) + " <br> Available bikestands: " + str(i[3])

    mycursor.close()
    mydb.close()
    return message


if __name__ == '__main__':
    app.run(debug=True, port=8000)

