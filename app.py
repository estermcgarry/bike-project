from flask_googlemaps import GoogleMaps
import mysql.connector
from flask import Flask, render_template
import json
import pickle

from sklearn.externals import joblib

app = Flask(__name__,  template_folder="./templates")

app.config['GOOGLEMAPS_KEY'] = "AIzaSyBR7esRJtzTOqcv53Bk3t1xpiCF0YPO-3I"
app.config['WEATHER_KEY'] = "https://api.darksky.net/forecast/313018b2afc91b7825d89c2740c19873/53.3498,-6.0"

# Initialize the extension
GoogleMaps(app)

@app.route('/')
def index():
    # Connecting to DB
    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )

    mycursor = mydb.cursor()

    # Joining 2 tables in our DB to get the info wer're using on your site
    mycursor.execute("""SELECT static.StationNumber,
    static.StationName,
    static.Latitude,
    static.Longitude,
    available_info.AvailableBikes,
    available_info.AvailableBikeStands
    FROM StaticData static
    INNER JOIN (
    select distinct t1.StationNumber,
                    t1.AvailableBikes,
                    t1.AvailableBikeStands
    from DynamicData t1
    inner join
    (select StationNumber, max(concat(date, ' ', time)) as max_date_time
    from DynamicData
    group by StationNumber) t2
    on t1.StationNumber = t2.StationNumber
                      and concat(t1.Date, ' ', t1.Time) = t2.max_date_time
    ) available_info on static.StationNumber = available_info.StationNumber
    ORDER BY static.StationName ASC""")

    markers = []
    station_names = []

    for i in mycursor:
        # Selecting all the information we need for features involving markers
        station = {"number": i[0], "name" : i[1], "latitude" : i[2], "longitude" : i[3], "available_bikes" : i[4], "available_bike_stands" : int(i[5])}
        markers.append(station)

        # Selecting information to be used in the dropdown menu
        infoDropdown = {"number": i[0], "name" : i[1]}
        station_names.append(infoDropdown)

    mycursor.close()

    weather_cursor = mydb.cursor()
    weather_cursor.execute("SELECT * FROM WeatherData WHERE Date=(SELECT max(Date) FROM WeatherData) ORDER BY Date DESC, Time DESC LIMIT 1;")

    #Store weather info into a dictionary
    weather_info = []
    for i in weather_cursor:
        info = {"Date": i[0], "Time": i[1], "Rainfall": i[2], "Temperature": i[3], "Icon": i[4],"WindSpeed": i[5]}
        weather_info.append(info)

    weather_cursor.close()
    mydb.close()

    # returning information to our index, making python variables available to be used in a HTML file
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

    # Getting information on Dabatabase from to display up to date info Windown for markers
    mycursor.execute("select StationNumber, StationName, AvailableBikes, AvailableBikeStands from DynamicData where StationNumber = " + station + " order by Date DESC, Time DESC limit 1;")
    message = "No information"
    for i in mycursor:
        # info Window - HTML
        message = "<b>" + i[1] + "</b> <br>Available bikes: " + str(i[2]) + " <br> Available bikestands: " + str(i[3] + " <br> <a href=\"javascript:getDirections()\">Directions</a>")
    mycursor.close()
    mydb.close()
    return message


@app.route('/station/<station>/<weekday>')
def prediction(station, weekday):

    # Assigns the weekday to its respective array
    if weekday == 0:
        weekday_list = [0,0,0,0,0,1]
    elif weekday == 1:
        weekday_list = [0,0,0,0,0,0]
    elif weekday == 2:
        weekday_list = [1,0,0,0,0,0]
    elif weekday == 3:
        weekday_list = [0,1,0,0,0,0]
    elif weekday == 4:
        weekday_list = [0,0,1,0,0,0]
    elif weekday == 5:
        weekday_list = [0,0,0,1,0,0]
    else:
        weekday_list = [0,0,0,0,1,0]

    # Division of stations per area
    area1=[3,7,9,10,16,17,18,28,29,31,37,45,47,48,51,53,54,58,64,65,69,74,75,80,82,91,95,97,102,108,109,110,116]
    area2=[2,4,5,6,8,11,12,13,19,21,22,23,24,27,30,32,33,36,39,40,41,42,44,49,50,52,55,56,57,59,61,63,68,71,72,73,76,79,83,84,85,86,87,88,89,90,92,93,94,96,98,99,101,103,104,105,107,111,112,113,115,117]
    area3=[15,25,26,34,38,43,62,66,67,77,78,81,100,106,114]

    # assigns each station number to its station area array
    if int(station) in area1:
        station_area = [0,0]
    elif int(station) in area2:
        station_area = [1,0]
    else:
        station_area = [0,1]


    # combaning the two arrays
    X_test = weekday_list + station_area
    # Transforming 1D array into a 2D array
    X_test = [X_test]

    # Load the model from the file
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

    # Use the loaded model to make predictions
    prediction = loaded_model.predict(X_test)

    # extracting the predicted number from the 2D array
    for i in prediction:
        for j in i:
            final_number = (int(round(j, 0)))

    # creating a message to add to the html
    message = "<b> We estimate " + str(final_number) + " available bikes for that day. </b>"
    
    return message

if __name__ == '__main__':
    #http
    app.run(host="0.0.0.0", port=80)

    #locally
    #app.run(debug=True, port=8000)

