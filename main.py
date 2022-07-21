# coding: utf-8
import requests

API_key = "7634767ba0fee7f3345a359625d2791c"

standort = input("PLZ: ")
land="de"
API_anfrage_url = "http://api.openweathermap.org/data/2.5/weather?zip="+standort+","+land+"&appid="+API_key



_anfrage = requests.get(API_anfrage_url)

wetterdaten= _anfrage.json()

windgeschwindigkeit = wetterdaten['wind']['speed']

windrichtung = wetterdaten['wind']['deg']

if 10 <= windrichtung < 30:
    windrichtung="NNO"
elif 30 <= windrichtung < 60:
    windrichtung="NO"
elif 60 <= windrichtung < 80:
    windrichtung="ONO"
elif 80 <= windrichtung < 100:
    windrichtung="O"
elif 100 <= windrichtung < 120:
    windrichtung="OSO"
elif 120 <= windrichtung < 150:
    windrichtung="SO"
elif 150 <= windrichtung < 170:
    windrichtung="SSO"
elif 170 <= windrichtung < 190:
    windrichtung="S"
elif 190 <= windrichtung < 210:
    windrichtung="SSW"
elif 210 <= windrichtung < 240:
    windrichtung="SW"
elif 240 <= windrichtung < 260:
    windrichtun="WSW"
elif 260 <= windrichtung < 280:
    windrichtung="W"
elif 280 <= windrichtung < 300:
    windrichtung="WNW"
elif 300 <= windrichtung < 330:
    windrichtung="NW"
elif 330 <= windrichtung < 350:
    windrichtung="NNW"
elif 350 <= windrichtung < 10:
    windrichtung="N"

print("Aktuelle Windgeschwindigkeit: ",windgeschwindigkeit,"m/s")
print("Windrichtung: ",windrichtung)


