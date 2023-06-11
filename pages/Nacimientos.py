import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import altair as alt

APP_TITLE = 'Nacimientos'
APP_SUB_TITLE = 'Fuente: Ine'

st.set_page_config(page_title=APP_TITLE, page_icon='👶', layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)

def display_time_filters(df):
    year_list = list(df['Periodo'].unique())
    year_list.sort(reverse = True )
    years = st.slider('Periodo', min_value=int(year_list[0]),  max_value=int(year_list[-1]), value=(2000, 2021))
    return years

def display_time_filter(df):
    year_list = list(df['Periodo'].unique())
    year_list.sort(reverse = True )
    years = st.slider('Periodo', min_value=int(year_list[0]),  max_value=int(year_list[-1]), value=2021)
    return years

def display_cs_filters(df, year):
    cs_list = list(df['Estado civil de la madre'].unique())
    cs = st.multiselect('Estado civil de la madre', cs_list)

    if len(cs) > 0: st.header(f'{year} - {cs}')
    return cs


def display_datos_nacimientos(df, years, cs):

    if len(cs)==0:
            st.error("Please select at least one country.")

    else:
        df = df[(df['Periodo'].between(years[0], years[1])) & (df['Estado civil de la madre'].isin(cs)) ]
        chart = (
                    alt.Chart(df)
                    .mark_line()
                    .encode(
                        x="Periodo",
                        y=alt.Y("Total:Q", stack=None),
                        color="Estado civil de la madre:N",
                    )
                )
        st.altair_chart(chart, use_container_width=True)    

def display_porcentajes(df, year):
    df = df[df['Periodo'] == year ]
    st.bar_chart(df, x='Estado civil de la madre', y='Total')

# prov_geo = 'data/provincias.geojson'
path_nacimientos = 'data/nacimientos.csv'
data = pd.read_csv(path_nacimientos, encoding='utf-8', sep=';')

years = display_time_filters(data)
cs = display_cs_filters(data, years)

display_datos_nacimientos(data, years, cs)


year = display_time_filter(data)
display_porcentajes(data, year)