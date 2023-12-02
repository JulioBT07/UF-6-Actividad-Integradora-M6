import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import plotly.express as px
import pydeck as pdk
import matplotlib.colors as mcolors


st.set_page_config(page_title="Police Incidents", page_icon=":police_car:",layout="wide")
st.title("Police Incident Reports from 2018 to 2020 in San Francisco :male-police-officer:")
df = pd.read_csv("Police.csv")
col1, col2 = st.columns(2)
col1.markdown("The data shown below  belongs to incident reports in the city of San francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police districts, neighborhood in which it happened, type of incidentin category and subcategory, exact location and resoluntion.")
mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
'Police District',
mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
'Neighborhood',
subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())

if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

col2.dataframe(subset_data)
st.divider()
st.markdown('It is important to mention that any police district can aswer to any incident, the neighborhood in which it happened is not related to the police distrcit')
st.markdown('Crime locations in San Francisco')
# Calcula la frecuencia de cada vecindario
neighborhood_counts = subset_data['Neighborhood'].value_counts()

# Crea un diccionario de colores para cada vecindario
colors_dict = {neighborhood: count for neighborhood, count in neighborhood_counts.items()}

# Crea el mapa con colores según la frecuencia de repeticiones de cada vecindario
fig = px.scatter_mapbox(
    subset_data,
    lat='lat',
    lon='lon',
    color='Neighborhood',
    color_continuous_scale=px.colors.sequential.Viridis,  # Puedes cambiar la paleta de colores aquí
    title='Mapa de Vecindarios',
)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig, use_container_width=True)
#st.map(subset_data)
st.markdown('Crimes ocurred per day of teh week')
fig = px.bar(subset_data, x='Day', color='Police District', title='Gráfico de Barras por Distrito Policial')
st.plotly_chart(fig, use_container_width=True)
subset_data['Date'] = pd.to_datetime(subset_data['Date'])
subset_data['Date'] = pd.to_datetime(subset_data['Date'])
min_date = subset_data['Date'].min()
max_date = subset_data['Date'].max()

columna1, columna2 = st.columns(2)
# Crea un input de fecha para el rango de fechas
selected_date_range1 = columna1.date_input('Selecciona una fecha de incio', (min_date))
selected_date_range2 = columna2.date_input('Selecciona una fecha final', (max_date))

# Convierte las fechas seleccionadas a datetime64[ns]
selected_date_range1 = (pd.to_datetime(selected_date_range1))
selected_date_range2 = (pd.to_datetime(selected_date_range2))

# Filtra el DataFrame por el rango de fechas seleccionado
filtered_df = subset_data[(subset_data['Date'] >= selected_date_range1)]
filtered_df = subset_data[(subset_data['Date'] <= selected_date_range2)]

st.markdown(f'Crime ocurred per date between {selected_date_range1} and {selected_date_range2}')
st.line_chart(filtered_df['Date'].value_counts())
st.markdown(f'Type of crimmes commited between {selected_date_range1} and {selected_date_range2}')
st.bar_chart(filtered_df['Incident Category'].value_counts())

agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())

st.divider()

años_disponibles = subset_data['Date'].dt.year.unique()

# Agregar un filtro de selección de año en Streamlit
selected_year = st.selectbox("Seleccione un año:", años_disponibles)
st.divider()
c1, c2 = st.columns(2)
df_filtrado = subset_data[subset_data['Date'].dt.year == selected_year]

columna1.markdown('Resolution status')
labels = df_filtrado['Resolution'].unique()
data_counts = df_filtrado['Resolution'].value_counts()

fig = px.pie(data_counts, names=labels, title='Distribución de Resoluciones',
             values=data_counts, labels=labels,
             template='seaborn', hole=0.5)  # Ajusta el valor de 'hole' para cambiar el tamaño del agujero donut

fig.update_traces(textinfo='percent+label', rotation=20)

c1.plotly_chart(fig)



# Extrae el mes y crea una nueva columna 'Month'
df_filtrado['Month'] = df_filtrado['Date'].dt.month_name()

# Cuenta la frecuencia de cada mes
month_counts = df_filtrado['Month'].value_counts()

# Crea el gráfico de pie
fig = px.pie(month_counts, names=month_counts.index, values=month_counts.values, title='Distribución de Crimenes por Mes')
c2.plotly_chart(fig, use_container_width=True)





