import streamlit as st
import requests
import datetime
import pandas as pd
import numpy as np
import geopy as gp

'''
# Calculate the Taxi Fare here!
'''


city = 'New York'
province = 'New York City'
country = 'United States'

date = st.sidebar.date_input('When are you travelling?', datetime.date(2019, 7, 6))
time = st.sidebar.time_input('Time to travel', datetime.time(8, 45))
from_street = st.sidebar.text_input('From where are you travelling?', "Hoboken")
to_street = st.sidebar.text_input('To where are you travelling?', "Hoboken")
n_passengers = st.sidebar.slider('Select number of passengers', 1, 10, 1)


# Processing location
geolocator = gp.Nominatim(user_agent="GTA Lookup")
location_to = geolocator.geocode(to_street+", "+city+", "+province+", "+country)
location_from = geolocator.geocode(to_street+", "+city+", "+province+", "+country)
lat_to = location_to.latitude
lon_to = location_to.longitude
lat_from = location_from.latitude
lon_from = location_from.longitude
travel_datetime = datetime.datetime.combine(date, time)
travel_datetime = travel_datetime.strftime("%Y-%m-%d %H:%M:%S")

# @st.cache
map_data = pd.DataFrame({'lat': [lat_from], 'lon': [lon_from]})
st.map(map_data, zoom=12)

params = {
    "pickup_datetime": travel_datetime,
    "pickup_longitude": lon_from,
    "pickup_latitude": lat_from,
    "dropoff_longitude": lon_to,
    "dropoff_latitude": lat_to,
    "passenger_count": n_passengers
    }

if st.sidebar.button('Calculate taxifare'):
    url = 'https://taxifare.lewagon.ai/predict'
    response = requests.get(url, params = params).json()
    fare = response['fare']
    st.markdown(f'Going from {from_street} to {to_street} with {n_passengers} passengers at {time} on {date}..')
    st.markdown(f'... your estimated fare is { fare }')
