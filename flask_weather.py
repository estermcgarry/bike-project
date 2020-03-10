#Flask send weather request to the database
import mysql.connector
from flask import Flask, render_template
import json

app = Flask(__name__,  template_folder="./templates")
app.config['WEATHER_KEY'] = 'https://api.darksky.net/forecast/313018b2afc91b7825d89c2740c19873/53.3498,-6.0'

#Connect to the database
@app.route('/')
def mapview():
    mydb = mysql.connector.connect(
        host="bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="picanha123",
        database='BikeData'
    )
    #Open a sql query
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Icon, Temperature, Rainfall, WindSpeed FROM WeatherData;")

    #Store info into a dictonary
    weather_info = []
    for i in mycursor:
        info = {"Icon": i[0], "Temperature": i[1], "Rainfall": i[2],"WindSpeed": i[3]}
        weather_info.append(info)

    #Close request
    mycursor.close()
    mydb.close()

    return render_template('index.html', weather_info=json.dumps(weather_info))

#Return content of weatherinfo.html file
@app.route('/weatherinfo')
def weatherinfo():
    return render_template('weatherinfo.html')

#Update changes automaticaly
if __name__ == '__main__':
    app.run(debug=True)

