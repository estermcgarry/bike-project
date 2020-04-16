import pickle

weekday_js = 1
station_num = 108

if weekday_js == 0:
    weekday = [0,0,0,0,0,1]
elif weekday_js == 1:
    weekday = [0,0,0,0,0,0]
elif weekday_js == 1:
    weekday = [1,0,0,0,0,0]
elif weekday_js == 1:
    weekday = [0,1,0,0,0,0]
elif weekday_js == 1:
    weekday = [0,0,1,0,0,0]
elif weekday_js == 1:
    weekday = [0,0,0,1,0,0]
else:
    weekday = [0,0,0,0,1,0]

area1=[3,7,9,10,16,17,18,28,29,31,37,45,47,48,51,53,54,58,64,65,69,74,75,80,82,91,95,97,102,108,109,110,116]
area2=[2,4,5,6,8,11,12,13,19,21,22,23,24,27,30,32,33,36,39,40,41,42,44,49,50,52,55,56,57,59,61,63,68,71,72,73,76,79,83,84,85,86,87,88,89,90,92,93,94,96,98,99,101,103,104,105,107,111,112,113,115,117]
area3=[15,25,26,34,38,43,62,66,67,77,78,81,100,106,114]

if station_num in area1:
    station_area = [0,0]
elif station_num in area2:
    station_area = [1,0]
else:
    station_area = [0,1]


X_test = weekday + station_area
X_test = [X_test]

# Load the model from the file
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

# Use the loaded model to make predictions
result = loaded_model.predict(X_test)

for i in result:
    print(i)
    for j in i:
        print(int(round(j, 0)))
