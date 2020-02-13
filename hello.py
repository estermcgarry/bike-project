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
