# coding: utf-8
import altair
import requests
import pandas as pd
import streamlit as st


# Layout der Startseite
st.set_page_config(
    page_title="Windvorhersage für Deutschland",
    layout="wide"
)
# columns für optik
col1, col2, col3 = st.columns([1, 2, 1])
col2.title('Winddaten für Deutschland')
form = col2.form(key='my_form', )
city = form.text_input(label='Stadtname:')
submit_button = form.form_submit_button(label='Los')


# Notwendige Daten beschaffen und transformieren mithilfe der API von 'openweathermap.com'.
# 2 Requests, einmal für die aktuellen Daten und dann nochmal für die Vorhersage.
#
def APIRequest(city):

    try:

        API_key = "7634767ba0fee7f3345a359625d2791c"

        land = "de"

        API_anfrage_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + land + "&appid=" + API_key

        wetterdaten = requests.get(API_anfrage_url).json()

        windgeschwindigkeit = wetterdaten['wind']['speed']

        windrichtung = wetterdaten['wind']['deg']

        himmelsrichtung = windrichtung_umrechner(windrichtung)

        API_anfrage_forecast = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "," + land + "&appid=" + API_key

        forecast = requests.get(API_anfrage_forecast).json()

    except:
        st.error("Stadt nicht gefunden.")

    lst_date = []
    lst_wind = []
    lst_date_time = []

    for i in range(0, len(forecast['list'])):
        _datedate_time = forecast['list'][i]['dt_txt']
        date_time = _datedate_time.split()
        lst_date.append(date_time[0])
        date_time_short = date_time[1].split(':')
        lst_date_time.append(date_time_short[0] + ":00")
        wind = forecast['list'][i]['wind']['speed']
        lst_wind.append(str(forecast['list'][i]['wind']['speed']))
    # listen mit pandas zu dataframe zusammenfügen
    df_winddaten = pd.DataFrame(list(zip(lst_date, lst_date_time, lst_wind)),
                                columns=['Datum', 'Uhrzeit', 'Windstärke in m/s'])

    # Objekt welches die Daten für die Vorhersage, aufgeteilt in die unterschiedlichen Tage, trägt.
    days_group = df_winddaten.groupby(["Datum"])

    return (days_group, windgeschwindigkeit, windrichtung, himmelsrichtung, city)


# Wird in APIRequest funktion verwendet um Himmelsrichtung festzulegen
def windrichtung_umrechner(windrichtung):
    if 10 <= windrichtung < 30:
        himmelsrichtung = "NNO"
    elif 30 <= windrichtung < 60:
        himmelsrichtung = "NO"
    elif 60 <= windrichtung < 80:
        himmelsrichtung = "ONO"
    elif 80 <= windrichtung < 100:
        himmelsrichtung = "O"
    elif 100 <= windrichtung < 120:
        himmelsrichtung = "OSO"
    elif 120 <= windrichtung < 150:
        himmelsrichtung = "SO"
    elif 150 <= windrichtung < 170:
        himmelsrichtung = "SSO"
    elif 170 <= windrichtung < 190:
        himmelsrichtung = "S"
    elif 190 <= windrichtung < 210:
        himmelsrichtung = "SSW"
    elif 210 <= windrichtung < 240:
        himmelsrichtung = "SW"
    elif 240 <= windrichtung < 260:
        _windrichtun = "WSW"
    elif 260 <= windrichtung < 280:
        himmelsrichtung = "W"
    elif 280 <= windrichtung < 300:
        himmelsrichtung = "WNW"
    elif 300 <= windrichtung < 330:
        himmelsrichtung = "NW"
    elif 330 <= windrichtung < 350:
        himmelsrichtung = "NNW"
    elif 350 <= windrichtung < 10:
        himmelsrichtung = "N"

    return (himmelsrichtung)


# Visualisierung der Daten. Die Spalten sind nur für den Aufbau da.
#
def cs_body(days_group, windgeschwindigkeit, windrichtung, himmelsrichtung, city):

    col_ol, col_l, col_r, col_or = st.columns([1, 1, 1, 1])

    col2.header('Aktuelle Winddaten für ' + city)

    col_l.metric("Aktuelle Windgeschwindigkeit: ", str(windgeschwindigkeit) + " m/s")

    col_r.metric("Aktuelle Windrichtung: ", str(windrichtung) + "° ", himmelsrichtung)

    st.header('Vorhersage')
    # Für jeden Tag der vorhersage wird eine Tabelle und ein Verlaufsdiagramm gezeichnet
    for name, group in days_group:
        group.drop(columns=['Datum'], inplace=True)
        split_name = name.split('-')

        with st.expander(split_name[2] + '.' + split_name[1] + '.' + split_name[0]):
            tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

            ts_chart_data = altair.Chart(group.astype({'Windstärke in m/s': 'float'})).mark_line(
                point=altair.OverlayMarkDef(color="orange")).encode(
                x=altair.X('Uhrzeit'),
                y=altair.Y('Windstärke in m/s'),
                tooltip='Windstärke in m/s').properties(width=270, height=0)

            tab1.altair_chart(ts_chart_data)

            styler = group.style.hide_index()
            tab2.write(styler.to_html(), unsafe_allow_html=True)


# Wenn der "submit button" gedrückt wird werden Daten angefordert, Transformiert, und anschließend Visualisiert.
if submit_button:
    var_lst = APIRequest(city)
    cs_body(var_lst[0], var_lst[1], var_lst[2], var_lst[3], var_lst[4])
