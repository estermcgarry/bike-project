from flask_googlemaps import GoogleMaps
import mysql.connector
from flask import Flask, render_template
import json

app = Flask(__name__,  template_folder="./templates")

app.config['GOOGLEMAPS_KEY'] = "AIzaSyBR7esRJtzTOqcv53Bk3t1xpiCF0YPO-3I"

# Initialize the extension
GoogleMaps(app)

@app.route("/")
def mapview():
    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT StationName, Latitude, Longitude FROM StaticData;")

    markers = []

    for i in mycursor:
        station = {"name" : i[0], "latitude" : i[1], "longitude" : i[2]}
        markers.append(station)

    mycursor.close()
    mydb.close()

    return render_template('template.html', markers=json.dumps(markers))

if __name__ == '__main__':
    app.run(debug=True)
#    app.run(host='0.0.0.0', port=5000)
