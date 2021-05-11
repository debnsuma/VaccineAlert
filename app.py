import streamlit as st 
from datetime import date
from pprint import pprint as pp

import requests
import json
import pandas as pd
import pydeck as pdk


def get_slot(pin_code, current_data):

    BASE_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}"
    URL = BASE_URL.format(pin_code, current_data)

    # Faking the browser header (http://www.useragentstring.com/pages/useragentstring.php?name=Chrome) 
    browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    response = requests.get(URL, headers=browser_header)
    data = json.loads(response.text)

    center = {}
    centers = [] 
    if data["sessions"]:
        for slots in data["sessions"]:
            center["Center Name"] = slots["center_id"]
            center["Address"] = slots["address"]
            center["Pin"] = slots["pincode"]
            center["Date"] = slots["date"]
            center["Vaccine Name"] = slots["vaccine"]
            center["Available Capacity"] = slots["available_capacity"]
            center["Available Slot"] = slots["slots"]   
            
            # for streamlite
            center["lat"] = slots["lat"] 
            center["long"] = slots["long"] 
            
            centers.append(center)
    else:
        centers = []
    
    return centers

st.title('CoWIN Vaccination Slot in my area')
st.info('The CoWIN APIs are geo-fenced so sometimes you may not see an output! Please try after sometime')
st.write("**Enter your PIN Code**")
pin_code = st.number_input("",value=110001)
current_data = date.today().strftime("%d-%m-%y")

st.write(pin_code)
data = get_slot(pin_code, current_data)

if data:
    st.write(f"**Here are the available slots as of {current_data}**")
    st.json(json.dumps(data))
    lat_lon = []
    for c in data:
        lat_lon.append([c["lat"], c["long"]])
    df = pd.DataFrame(lat_lon, columns=['lat', 'lon'])

    st.write(f"**Exact location of the center**")
    st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=28,
         longitude=77,
         zoom=11,
         pitch=50,
     ),
     layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))

else:
    st.write("**Sorry no slot available :( Try after sometime! **")


