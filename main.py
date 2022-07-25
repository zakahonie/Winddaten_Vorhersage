# coding: utf-8
import requests
import numpy as np
import pandas as pd

API_key = "7634767ba0fee7f3345a359625d2791c"

standort = input("PLZ: ")

land="de"

API_anfrage_url = "http://api.openweathermap.org/data/2.5/weather?zip="+standort+","+land+"&appid="+API_key

_anfrage = requests.get(API_anfrage_url)

wetterdaten = _anfrage.json()

windgeschwindigkeit = wetterdaten['wind']['speed']

windrichtung = wetterdaten['wind']['deg']

#32683----

API_anfrage_forecast = "http://api.openweathermap.org/data/2.5/forecast?zip="+standort+","+land+"&appid="+API_key

_forecast = requests.get(API_anfrage_forecast)

forecast = _forecast.json()



lst_date = []
lst_wind = []
lst_time = []
i = 0

for i in range(0, len(forecast['list'])) :
    _datetime = forecast['list'][i]['dt_txt']
    time = _datetime.split()
    lst_date.append(time[0])
    lst_time.append(time[1])
    lst_wind.append(forecast['list'][i]['wind']['speed'])

df_winddaten = pd.DataFrame(list(zip(lst_date, lst_time, lst_wind)),
               columns =['Datum', 'Uhrzeit','Windstaerke'])

print(df_winddaten)


if 10 <= windrichtung < 30:
    _windrichtung="NNO"
elif 30 <= windrichtung < 60:
    _windrichtung="NO"
elif 60 <= windrichtung < 80:
    _windrichtung="ONO"
elif 80 <= windrichtung < 100:
    _windrichtung="O"
elif 100 <= windrichtung < 120:
    _windrichtung="OSO"
elif 120 <= windrichtung < 150:
    _windrichtung="SO"
elif 150 <= windrichtung < 170:
    _windrichtung="SSO"
elif 170 <= windrichtung < 190:
    _windrichtung="S"
elif 190 <= windrichtung < 210:
    _windrichtung="SSW"
elif 210 <= windrichtung < 240:
    _windrichtung="SW"
elif 240 <= windrichtung < 260:
    _windrichtun="WSW"
elif 260 <= windrichtung < 280:
    _windrichtung="W"
elif 280 <= windrichtung < 300:
    _windrichtung="WNW"
elif 300 <= windrichtung < 330:
    _windrichtung="NW"
elif 330 <= windrichtung < 350:
    _windrichtung="NNW"
elif 350 <= windrichtung < 10:
    _windrichtung="N"

print("Aktuelle Windgeschwindigkeit: ",windgeschwindigkeit,"m/s")
print("Windrichtung: ",windrichtung,"° ,",_windrichtung)

print(API_anfrage_forecast)
