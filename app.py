import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import locale
import requests
from urllib.request import urlopen
import json
from streamlit_echarts import st_echarts
from urllib.error import URLError
from datetime import datetime
from dateutil import parser

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
@st.cache
def from_data_file(filename):
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename)
    return pd.read_json(url)

def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


option = st.sidebar.selectbox(
    'Menu:',
    ('Home', 'Persebaran Covid', 'Data Vaksin','Data Rumah Sakit')
)

if option == 'Home' or option == '':
    st.write("""# Dokumentasi Covid-19 Indonesia""")  # menampilkan halaman utama
elif option == 'Persebaran Covid1':
    st.write("""## Peta Persebaran Covid-19 di Indonesia""")  # menampilkan judul halaman dataframe

    try:
        ALL_LAYERS = {
            # "Bike Rentals": pdk.Layer(
            #     "HexagonLayer",
            #     data=from_data_file("bike_rental_stats.json"),
            #     get_position=["lon", "lat"],
            #     radius=200,
            #     elevation_scale=4,
            #     elevation_range=[0, 1000],
            #     extruded=True,
            # ),
            # "Bart Stop Exits": pdk.Layer(
            #     "ScatterplotLayer",
            #     data=from_data_file("bart_stop_stats.json"),
            #     get_position=["lon", "lat"],
            #     get_color=[200, 30, 0, 160],
            #     get_radius="[exits]",
            #     radius_scale=0.05,
            # ),
            # "Bart Stop Exit": pdk.Layer(
            #     "ScatterplotLayer",
            #     data=pd.read_json(
            #         "https://raw.githubusercontent.com/streamlit/example-data/master/hello/v1/bart_stop_stats.json"),
            #     get_position=["lon", "lat"],
            #     get_color=[200, 30, 0, 160],
            #     get_radius="[exits]",
            #     radius_scale=0.05,
            # ),

            # "Bart Stop Names": pdk.Layer(
            #     "TextLayer",
            #     data=pd.read_json(
            #         'https://data.covid19.go.id/public/api/prov.json'),
            #     get_position=["list_data['lokasi']['lon']",
            #                   "list_data['lokasi']['lat']"],
            #     get_text="name",
            #     get_color=[0, 0, 0, 200],
            #     get_size=15,
            #     get_alignment_baseline="'bottom'",
            # ),
            "Banyak Kasus": pdk.Layer(
                "ScatterplotLayer",
                data=pd.read_json(
                    'https://apicovid19indonesia-v2.vercel.app/api/indonesia/provinsi/more'),
                get_position=["lokasi['lon']",
                              "lokasi['lat']"],
                get_color=[200, 30, 0, 160],
                get_radius="[kasus]",
                radius_scale=0.1,
                pickable=True,
            ),
        }
        st.sidebar.markdown('### Peta:')
        selected_layers = [
            layer for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)]
        if selected_layers:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": -3.6687994,
                                    "longitude": 119.9740534, "zoom": 3.5, "pitch": 0},
                layers=selected_layers,
                tooltip={"html": "{provinsi}<b><br>{kasus}</b>"}
            ))
        else:
            st.error("Centang bagian Banyak Kasus untuk melihat peta!")
    except URLError as e:
        st.error("""
            **This demo requires internet access.**

            Connection error: %s
        """ % e.reason)
elif option == 'Data Vaksin':
    st.write("""## Data Vaksinasi di Indonesia""")  # menampilkan judul halaman

    # membuat variabel chart data yang berisi data dari dataframe
    # data berupa angka acak yang di-generate menggunakan numpy
    # data terdiri dari 2 kolom dan 20 baris
    # chart_data = pd.DataFrame(
    #     np.random.randn(20,2),
    #     columns=['a','b']
    # )
    # #menampilkan data dalam bentuk chart
    # st.line_chart(chart_data)
    # #data dalam bentuk tabel
    # chart_data

    url = "https://vaksincovid19-api.vercel.app/api/vaksin"

    # store the response of URL
    response = urlopen(url)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())

    data = pd.DataFrame(data_json, index=[0])
    # data.set_index('')
    totalsasaran =data['totalsasaran'][0]

    sasaranvaksinsdmk = data['sasaranvaksinsdmk'][0]
    sasaranvaksinlansia= data['sasaranvaksinlansia'][0]
    sasaranvaksinpetugaspublik= data['sasaranvaksinpetugaspublik'][0]
    vaksinasi1= data['vaksinasi1'][0]
    vaksinasi2= data['vaksinasi2'][0]
    lastUpdate = data['lastUpdate'][0]
    # df
    class NpEncoder(json.JSONEncoder):

        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super(NpEncoder, self).default(obj)
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Data Vaksinasi di Indonesia",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": [
                    {"value": json.dumps(sasaranvaksinlansia, cls=NpEncoder), "name": "Lansia"},
                    {"value": json.dumps(sasaranvaksinsdmk,cls=NpEncoder), "name": "SDMK"},
                    {"value": json.dumps(sasaranvaksinpetugaspublik, cls=NpEncoder),
                     "name": "Petugas Publik"},
                ],
            }
        ],
    }
    

    options1 = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
        },
        "legend": {"data": ["Vaksin1", "Vaksin2"]},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": [
            {
                "type": "category",
                "boundaryGap": False,
                "data": ["","Vaksinasi 1", "Vaksinasi 2"],
            }
        ],
        "yAxis": [{"type": "value"}],
        "series": [
            {
                "name": "Vaksinasi",
                "type": "line",
                "stack": "总量",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": [0,json.dumps(vaksinasi1, cls=NpEncoder), json.dumps(vaksinasi2, cls=NpEncoder)],
            },
        ],
    }

    sasaran = locale.format("%d", int(totalsasaran), grouping=True)

    col1, col2 = st.columns(2)
    tgl = parser.parse(lastUpdate).strftime("%d %B %Y %H:%M")
    
    col1.metric(label="Latest Update:",value="",delta=tgl)
    col2.metric(label="Total Sasaran:", value= sasaran +" orang")

    st_echarts(options=options, height="600px")
    st_echarts(options=options1, height="400px")

elif option == 'Persebaran Covid':
    st.write("""## Persebaran Covid-19 di Indonesia""")

    data = pd.read_json(
        'https://apicovid19indonesia-v2.vercel.app/api/indonesia/provinsi/more  ')
    df = data.set_index('provinsi')

    try:
        # df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index)
        )
        if not countries:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": -3.6687994,
                                    "longitude": 119.9740534, "zoom": 3.5, "pitch": 0},
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=data,
                        get_position=["lokasi['lon']",
                                      "lokasi['lat']"],
                        get_color=[200, 30, 0, 160],
                        get_radius="[kasus]",
                        radius_scale=0.1,
                        pickable=True,
                    ),
                ],
                tooltip={"html": "{provinsi}<b><br>{kasus} kasus</b>"}
            ))

        else:
            
            data1 = df.loc[countries]
            data = data1[["dirawat", "sembuh", "meninggal"]]
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            # data = data.T.reset_index()
            # data = pd.melt(data, id_vars=["index"]).rename(
            #     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            # )
            st.bar_chart(data)
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": -3.6687994,
                                    "longitude": 119.9740534, "zoom": 3.5, "pitch": 0},
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=data1,
                        get_position=["lokasi['lon']",
                                      "lokasi['lat']"],
                        get_color=[200, 30, 0, 160],
                        get_radius="[kasus]",
                        radius_scale=0.1,
                        pickable=True,
                    ),
                ],
                tooltip={"html": "Total Kasus = <b>{kasus} orang</b>"}
            ))
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

elif option == 'Data Rumah Sakit':
    
    st.write("""## Data Rumah Sakit Per Provinsi""")

    col1, col2 = st.columns(2)

    with col1:
        dfprov = pd.read_json(
            'https://rs-bed-covid-api.vercel.app/api/get-provinces')
        dataprov = pd.json_normalize(dfprov['provinces'])
        # dataprov

        def format_func(option):
            return dataprov.loc[option]['name']

        provinsis = st.selectbox(
            "Choose countries", options=list(dataprov.index), format_func=format_func
        )

        prov = dataprov.loc[provinsis]['id']

        dfkabkot = pd.read_json(
            'https://rs-bed-covid-api.vercel.app/api/get-cities?provinceid='+str(prov))
        datakabkot = pd.json_normalize(dfkabkot['cities'])
        # datakabkot

        def format_func2(option):
            return datakabkot.loc[option]['name']

        kabkotas = st.selectbox(
            "Choose cities", options=list(datakabkot.index), format_func=format_func2
        )

        kabkot = datakabkot.loc[kabkotas]['id']

    with col2:
        CHOICES = {1: "Rumah Sakit Covid", 2: "Rumah Sakit Non Covid"}

        def format_func3(option):
            return CHOICES[option]

        option = st.selectbox("Select option", options=list(CHOICES.keys()), format_func=format_func3)

        dfrs = pd.read_json(
            'https://rs-bed-covid-api.vercel.app/api/get-hospitals?provinceid='+str(prov)+'&cityid='+str(kabkot)+'&type='+str(option))
        datars = pd.json_normalize(dfrs['hospitals'])

        if not datars.empty:
            # st.write("### Rumah Sakit", datars)

            def format_func4(option):
                return datars.loc[option]['name']

            rses = st.selectbox(
                "Choose hospitals", options=list(datars.index), format_func=format_func4
                )
            
            rs = datars.loc[rses]['id']
            # rs

            dfrsbed = pd.read_json('https://rs-bed-covid-api.vercel.app/api/get-bed-detail?hospitalid='+str(rs)+'&type='+str(option))
            # dfrsbed
            datarsbed = pd.json_normalize(dfrsbed['data']['bedDetail'])
            datarsbed = datarsbed[["stats.title", "stats.bed_available", "stats.bed_empty","stats.queue"]]
            datarsbed.rename(columns={'stats.title':'Nama','stats.bed_available': 'Ketersediaan', 'stats.bed_empty': 'Kosong', 'stats.queue': 'Antrian'}, inplace=True)
            
    if datars.empty:
        st.error("Data tidak ditemukan")
    else:
        datarsbed

        dfmap = pd.read_json(
            'https://rs-bed-covid-api.vercel.app/api/get-hospital-map?hospitalid='+str(rs))

        datamap = dfmap['data']

        data = {'lat': [float(datamap['lat'])], 'lon': [
            float(datamap['long'])], 'name': [datamap['name']], 'address': [datamap['address']]}

        df = pd.DataFrame(data)

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=float(datamap['lat']),
                longitude=float(datamap['long']),
                zoom=11,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    pickable=True,
                    data=df,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
            tooltip={"html": "<b>{name}<br>{address}</b>"}
        ))
