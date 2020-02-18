#This code creates a function that requests JCDecaux dynamic data

#Create variables and assign its values




name = "dublinbike"
station_url = "https://api.jcdecaux.com/vls/v1/stations"
request = requests.get/(station_url, params={"apikey": api, "contract": name})
api = ""






url='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=28c31a8964f03149402ab48b7cd02cc9079481f7'
json_dataset = requests.get(url).text
test = json.loads(json_dataset)







# name = "" ???
# station = PUT THE URL???
# apibike = ???
#
#Define function
def mainfunc():
    # run in a infinity loop
    # while true:
        try:
            #get data from json file
            request = requests.get(stations, param={"apikey":, "contract":})

            #store the information into database
            store(json.loads(r.text))

            #put to sleep for 5 min even if exception occurs
            time.sleep(5*60)
        except:
            #If exception occurs, print the traceback
            print traceback.format_exc()

    return

#