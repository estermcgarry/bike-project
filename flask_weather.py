#Flask send weather request to the database
import mysql.connector
from flask import Flask, render_template
import json

app = Flask(__name__,  template_folder="./templates")
app.config['WEATHER_KEY'] = 'https://api.darksky.net/forecast/313018b2afc91b7825d89c2740c19873/53.3498,-6.0'

#Request weather information from database
@app.route('/')
def requestweather():
    #Connect to the database
    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )
    #Open a sql query
    mycursor = mydb.cursor()

    mycursor.execute("SELECT Date, Time, Icon, Temperature, Rainfall, WindSpeed FROM WeatherData;")

    #Store info into a dictionary
    weather_info = []
    for i in mycursor:
        info = {"Date": i[0], "Time": i[1], "Icon": i[2], "Temperature": i[3], "Rainfall": i[4],"WindSpeed": i[5]}
        weather_info.append(info)

    #Close request
    mycursor.close()
    mydb.close()

    #Store information in a variable
    return render_template('template.html', weather_info=json.dumps(weather_info))

#Update changes automaticaly
if __name__ == '__main__':
    app.run(debug=True, port=8000)


