import requests
import json

url='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=28c31a8964f03149402ab48b7cd02cc9079481f7'

json_dataset = requests.get(url).text

print(json_dataset)
test = json.loads(json_dataset)

for i in test:
    #print(i)
    print('Number: ', i['number'])
    print('Name: ', i['name'])
    print('Address: ', i['address'])
    print('Position: ')
    print('Latitude: ', i['position']['lat'])
    print('Longitude: ', i['position']['lng'])
    print('Banking: ', i['banking'])
    print('Bonus: ', i['bonus'])
    print('Bike Stands: ', i['bike_stands'])
    print('Available bike stands: ', i['available_bike_stands'])
    print('Available bikes: ', i['available_bikes'])
    print()


    #print(type(i))
with open("json_test.json", "w") as outfile:
    outfile.write(json_dataset)

url_weather='http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=7466c05583646392fcd053e5d7ba2edd'

json_dataset_weather = requests.get(url_weather).text

with open("weather_api.json", "w") as outfile:
    outfile.write(json_dataset_weather)
print(json_dataset_weather)

weather_test = json.loads(json_dataset_weather)
print(type(weather_test))
for i in weather_test:
    print(i)

    # print(json_dataset_weather["list"])
    # print('Number: ', i['number'])
    # print('Name: ', i['name'])
    # print('Address: ', i['address'])
    # print('Position: ')
    # print('Latitude: ', i['position']['lat'])
    # print('Longitude: ', i['position']['lng'])
    # print('Banking: ', i['banking'])
    # print('Bonus: ', i['bonus'])
    # print('Bike Stands: ', i['bike_stands'])
    # print('Available bike stands: ', i['available_bike_stands'])
    # print('Available bikes: ', i['available_bikes'])
    # print()