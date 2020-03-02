from flask import Flask
from flask_googlemaps import GoogleMaps
import mysql.connector
from flask_googlemaps import Map
from flask import Flask, render_template
import gmaps


app = Flask(__name__,  template_folder=".")
# gmaps.configure(api_key='AIzaSyBR7esRJtzTOqcv53Bk3t1xpiCF0YPO-3I')

app.config['GOOGLEMAPS_KEY'] = "AIzaSyBR7esRJtzTOqcv53Bk3t1xpiCF0YPO-3I"

# Initialize the extension
GoogleMaps(app)

@app.route('/')
def hello_world():
    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT StationName, Latitude, Longitude FROM StaticData;")
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    return "x"


@app.route("/ester")
def mapview():
    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT StationName, Latitude, Longitude FROM StaticData;")


    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=53.3476222,
        lng=-6.2606207,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "<b>Hello World from other place</b>"
            }
        ]
    )

    sndmap.markers = []

    # import json
    #
    # data = {}
    #     data['key'] = 'value'
    #     json_data = json.dumps(data)

    for (StationName, Latitude, Longitude) in mycursor:
        station = {}
        station['icon'] = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
        station['lat'] = Latitude
        station['lng'] = Longitude
        station['infobox'] = StationName
        sndmap.markers.append(station)


    mycursor.close()
    mydb.close()

    return render_template('template.html', mymap=mymap, sndmap=sndmap)

if __name__ == "__main__":
    app.run(debug=True)




host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
user="admin",
passwd="picanha123",
database='BikeData'
port = "3306"



def connect_to_database():
    engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(user,
                                                                   passwd,
                                                                   host,
                                                                   port,
                                                                   database), echo=True)
    return engine