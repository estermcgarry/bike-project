from flask_googlemaps import GoogleMaps
import mysql.connector
from flask import Flask, render_template
import json

app = Flask(__name__,  template_folder="./templates")

app.config['GOOGLEMAPS_KEY'] = "AIzaSyBR7esRJtzTOqcv53Bk3t1xpiCF0YPO-3I"

# Initialize the extension
GoogleMaps(app)



@app.route('/')
def mapview():

    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT StationNumber, StationName, Latitude, Longitude FROM StaticData;")

    markers = []

    for i in mycursor:
        station = {"number": i[0], "name" : i[1], "latitude" : i[2], "longitude" : i[3]}
        markers.append(station)

    mycursor.close()
    mydb.close()

    return render_template('index.html', markers=json.dumps(markers))

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


@app.route('/stations')
def stations():
    return render_template('stations.html')

@app.route('/contact')

def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)

