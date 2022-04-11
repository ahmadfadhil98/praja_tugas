import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import locale
from streamlit_echarts import st_echarts
from urllib.error import URLError
from datetime import datetime
from dateutil import parser

locale.setlocale(locale.LC_ALL, 'en_US')
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
    'Silakan pilih:',
    ('Home', 'Persebaran Covid', 'Data Vaksin')
)

if option == 'Home' or option == '':
    st.write("""# Halaman Utama""")  # menampilkan halaman utama
elif option == 'Persebaran Covid':
    st.write("""## Persebaran Covid""")  # menampilkan judul halaman dataframe

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
                    'https://data.covid19.go.id/public/api/prov.json'),
                get_position=["list_data['lokasi']['lon']",
                              "list_data['lokasi']['lat']"],
                get_color=[200, 30, 0, 160],
                get_radius="[list_data['jumlah_kasus']]",
                radius_scale=0.05,
            ),
            # "Outbound Flow": pdk.Layer(
            #     "ArcLayer",
            #     data=from_data_file("bart_path_stats.json"),
            #     get_source_position=["lon", "lat"],
            #     get_target_position=["lon2", "lat2"],
            #     get_source_color=[200, 30, 0, 160],
            #     get_target_color=[200, 30, 0, 160],
            #     auto_highlight=True,
            #     width_scale=0.0001,
            #     get_width="outbound",
            #     width_min_pixels=3,
            #     width_max_pixels=30,
            # ),
        }
        st.sidebar.markdown('### Map Layers')
        selected_layers = [
            layer for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)]
        if selected_layers:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": -3.6687994,
                                    "longitude": 119.9740534, "zoom": 3, "pitch": 50},
                layers=selected_layers,
            ))
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error("""
            **This demo requires internet access.**

            Connection error: %s
        """ % e.reason)
    # membuat dataframe dengan pandas yang terdiri dari 2 kolom dan 4 baris data
    df = pd.DataFrame({
        'Column 1': [1, 2, 3, 4],
        'Column 2': [10, 12, 14, 16]
    })
    # df  # menampilkan dataframe
elif option == 'Data Vaksin':
    st.write("""## Data Vaksin di Indonesia""")  # menampilkan judul halaman

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

    data = pd.read_json(
        'vaksin.json', orient='index')
    # data.set_index('')
    totalsasaran =data.loc['totalsasaran'][0]

    sasaranvaksinsdmk = data.loc['sasaranvaksinsdmk'][0]
    sasaranvaksinlansia= data.loc['sasaranvaksinlansia'][0]
    sasaranvaksinpetugaspublik= data.loc['sasaranvaksinpetugaspublik'][0]
    vaksinasi1= data.loc['vaksinasi1'][0]
    vaksinasi2= data.loc['vaksinasi2'][0]
    lastUpdate = data.loc['lastUpdate'][0]
    # df
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Data Vaksin di Indonesia",
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
                    {"value": sasaranvaksinlansia, "name": "Lansia"},
                    {"value": sasaranvaksinsdmk, "name": "SDMK"},
                    {"value": sasaranvaksinpetugaspublik, "name": "Petugas Publik"},
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
                "data": [0,vaksinasi1, vaksinasi2],
            },
        ],
    }

    sasaran = locale.format("%d", int(totalsasaran), grouping=True)

    col1, col2 = st.columns(2)
    tgl = parser.parse(lastUpdate).strftime("%d %B %Y %H:%M")
    
    col1.metric(label="Update",value="",delta=tgl)
    col2.metric(label="Total Sasaran", value= sasaran +" orang")

    st_echarts(
        options=options, height="500px",
    )
    st_echarts(options=options1, height="400px")

