# coding: utf-8
import requests

API_key = "7634767ba0fee7f3345a359625d2791c"
standort = "32683"
API_anfrage_url = "http://api.openweathermap.org/data/2.5/weather?zip="+standort+",de&appid="+API_key

print(API_anfrage_url)