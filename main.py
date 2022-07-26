# coding: utf-8
import altair
import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Windvorhersage für Deutschland",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('5 Tage Windvorhersage')
form = st.form( key='my_form',)
plz = form.text_input(label='PLZ eingeben:', max_chars=5)
submit_button = form.form_submit_button(label='Enter')

def APIRequest(plz):

    API_key = "7634767ba0fee7f3345a359625d2791c"

    land="de"

    API_anfrage_url = "http://api.openweathermap.org/data/2.5/weather?zip="+plz+","+land+"&appid="+API_key

    _anfrage = requests.get(API_anfrage_url)

    wetterdaten = _anfrage.json()

    windgeschwindigkeit = wetterdaten['wind']['speed']

    windrichtung = wetterdaten['wind']['deg']



    API_anfrage_forecast = "http://api.openweathermap.org/data/2.5/forecast?zip="+plz+","+land+"&appid="+API_key

    _forecast = requests.get(API_anfrage_forecast)
    forecast = _forecast.json()



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





#..... FORECAST.........................

    time_short = []
    lst_date = []
    lst_wind = []
    lst_time = []
    i = 0

    for i in range(0, len(forecast['list'])) :
        _datetime = forecast['list'][i]['dt_txt']
        time = _datetime.split()
        lst_date.append(time[0])
        time_short = time[1].split(':')
        lst_time.append(time_short[0]+":00")

        lst_wind.append(forecast['list'][i]['wind']['speed'])



    df_winddaten = pd.DataFrame(list(zip(lst_date, lst_time, lst_wind)),
               columns =['Datum', 'Uhrzeit','Windstärke in m/s'])


    days_group = df_winddaten.groupby(["Datum"])

    return(days_group, windgeschwindigkeit, windrichtung, _windrichtung, plz)




def cs_body(days_group, windgeschwindigkeit, windrichtung, _windrichtung, plz):
    st.title('Winddaten für '+plz)

    st.metric("Aktuelle Windgeschwindigkeit: ", str(windgeschwindigkeit)+" m/s")

    st.metric("Aktuelle Windrichtung: ", str(windrichtung)+"° ", _windrichtung)

    st.header('Vorhersage')
    for name, group in days_group:
            # print(name)
            # print(group)
            group.drop(columns=['Datum'], inplace=True)

            st.subheader('Datum: ' + name)
            tab1, tab2 = st.tabs(["🗃 Data", "📈 Chart"])
            tab1.write(group)

            ts_chart_data = altair.Chart(group).mark_line().encode(
                x=altair.X('Uhrzeit'),
                y=altair.Y('Windstärke in m/s')).properties(width=300, height=250)

            tab2.altair_chart(ts_chart_data)

if submit_button:

    var_lst = APIRequest(plz)
    cs_body(var_lst[0], var_lst[1], var_lst[2], var_lst[3], var_lst[4])



