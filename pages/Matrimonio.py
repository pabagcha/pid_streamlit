import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Matrimonios por provincias, sexo y Año'
APP_SUB_TITLE = 'Fuente: Ine'

st.set_page_config(page_title=APP_TITLE, page_icon='👭', layout="centered", initial_sidebar_state="auto", menu_items=None)

def display_time_filters(df):
    year_list = list(df['Periodo'].unique())
    year_list.sort(reverse = True )
    year = st.sidebar.selectbox('Periodo', year_list, 0)
    return year

def display_prov_filter(df, prov):
    return st.sidebar.selectbox('Provincia', prov_list)

def display_sex_filter(year):
    if year >= 2005:
        sex =  st.sidebar.radio('Sexo', ['Entre hombre y mujer', 'Entre hombres', 'Entre mujeres'])
    else:
        sex =  st.sidebar.radio('Sexo', ['Entre hombre y mujer'])
    
    
    st.header(f'{year} - {sex}' )
    return sex

def display_map(df, year, sex):
    df = df[(df['Periodo'] == year)  & (df['Sexo'] == sex)]
    df = df.drop(df[df['Provincias'] == 'Total'].index)

    m = folium.Map(location=[40.42,  -3.7], zoom_start=5)
    coropletas = folium.Choropleth(geo_data=prov_geo,name="choropleth",data=df,columns=["codigo", "Total"],key_on="properties.codigo", fill_color="YlGn",fill_opacity=0.7,line_opacity=1.0,legend_name="Nº de Matrimonios")
    coropletas.add_to(m)
    for feature in coropletas.geojson.data['features']:
       code = feature['properties']['codigo']
       feature['properties']['Provincias'] = prov_dict[code]
    coropletas.geojson.add_child(folium.features.GeoJsonTooltip(['Provincias'], labels=False))
    
    folium.LayerControl().add_to(m)
    st_map = st_folium(m, width=700, height=450)
    codigo = '00'
    if st_map['last_active_drawing']:
        codigo = st_map['last_active_drawing']['properties']['codigo']
    return codigo

def display_datos_matrimonios(df, year, sex, prov_name):
    df = df[(df['Periodo'] == year) & (df['Sexo'] == sex) & (df['Provincias'] == prov_name)]
    valor =  df.Total.iat[0]
    st.metric(sex, str(valor))
    return valor

    
st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)

prov_geo = 'data/provincias.geojson'
prov_matr = 'data/matrimonios.csv'
prov_data = pd.read_csv(prov_matr, encoding='utf-8', sep=';')
prov_data = prov_data.drop(prov_data[prov_data['Provincias'] == 'No residente'].index)
prov_data['codigo'] = prov_data['Provincias'].apply(lambda x: x[:2])
prov_data.fillna(0,inplace=True)

prov_list = list(prov_data['Provincias'].unique())
prov_dict = pd.Series(prov_data.Provincias.values,index=prov_data.codigo).to_dict()

year = display_time_filters(prov_data)
sex = display_sex_filter(year)

prov_code = display_map(prov_data, year, sex)
prov_name = display_prov_filter(prov_data, '')

if (prov_code!='00'):
    prov_name = prov_dict[prov_code]

st.subheader(f'Matrimonios: {prov_name}')    

col1, col2, col3 = st.columns(3)
with col1:
    heteros = display_datos_matrimonios(prov_data, year, 'Entre hombre y mujer', prov_name)
with col2:
    if year >=2005: 
        gays =display_datos_matrimonios(prov_data, year, 'Entre hombres', prov_name)
    else: gays=0
with col3:
    if year >=2005:
        lesbianas =display_datos_matrimonios(prov_data, year, 'Entre mujeres', prov_name)
    else: lesbianas = 0

total = heteros + gays + lesbianas
temp = pd.DataFrame(data={'Sexo': ['Hombre y mujer', 'Hombres', 'Mujeres'], '%':[100*heteros/total, 100*gays/total, 100*lesbianas/total]})
st.bar_chart(temp, x='Sexo', y='%')