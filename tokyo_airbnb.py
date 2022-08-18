import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
from IPython.display import HTML
import plotly.io as pio

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("# Streamlit Análisis y visualización de datos de Tokyo_Airbnb")
st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg")
# <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg" style= "height:150px;float:left;">

#leer datos
datos = pd.read_csv('tokyo_airbnb.csv')
st.markdown("# Exploración básica del dataset")
datos

st.markdown("### Descubierto por una simple descripción de los datos:")
st.markdown("""
            - Hay 14 columnas de características en total, cada una con11466 datos.
            - Hay 4 columnas con algún grado de falta (host_name/neighbourhood_group/last_review/reviews_per_month)
            """)

st.markdown("### Después de limpiar los datos:")
with st.echo():
    datos['host_name'].fillna(0,inplace = True)
    datos['last_review'].fillna(0,inplace = True)
    datos['reviews_per_month'].fillna(0,inplace = True)
    datos = datos.drop(columns='neighbourhood_group')
datos

st.markdown("#### Primero, un procesamiento simple y descripción de algunas características.")
st.write(datos['neighbourhood'].unique())
st.markdown("#### Hay tres tipos de habitaciones en total: conjunto completo, habitación individual y habitación para varias personas.")
st.write(datos['room_type'].unique())
st.markdown("#### El análisis de las salas muestra que la mayoría de ellas se alquilan en conjunto, y pocas salas públicas se alquilan.")
plt.subplot(311)
data = datos['room_type'].value_counts().tolist()
a = datos['room_type'].unique()
plt.bar(x=a, height=data)
st.pyplot()
st.markdown("#### Se puede ver que host_name está relativamente concentrado, lo que puede confirmar la conclusión extraída en las listas de host_calculadas en el tipo continuo anterior.Vamos a verlo en detalle.")
st.write(datos[['host_name','name']].groupby('host_name').count().sort_values(by='name', ascending=False))
st.markdown("#### La ubicación de la casa de familia está relativamente concentrada, aquí hay una mirada específica a las áreas. ")
datos['neighbourhood'].value_counts()
datos['neighbourhood'].value_counts().index[0]
st.markdown("""
            - La mayoría de las casas se concentran en el distrito de 'Shinjuku Ku', 'Taito Ku' y 'Toshima Ku'  .
            - El tipo de habitación se basa básicamente en todo el grupo, complementado con una habitación individual, hay menos habitaciones para varias personas
            """)
st.markdown("#### Explorar Metas：")
st.markdown("""
            - Región (distribución, precio).
            - Casas de familia (top 10 casas de familia más populares, cuáles son las características de las casas de familia más populares)
            - Perspectiva del arrendador (clasificación de los tipos de arrendadores, estimaciones de los ingresos de los arrendadores)
            """)
token = 'pk.eyJ1Ijoid2VubGxhIiwiYSI6ImNsNnhmcjFmcjBzbjQzZHFsNXB3YXc0cHAifQ.Yhi8lAIuVUiXA8TltkAMIw'
px.set_mapbox_access_token(token)

fig = px.scatter_mapbox(datos,
                        lat=datos['latitude'],
                        lon=datos['longitude'],
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        size_max=15,
                        zoom=9
                       )
st.plotly_chart(fig)

values = datos.neighbourhood.value_counts()
names = datos.neighbourhood.unique().tolist()
fig = px.pie(datos, values=values, names=names, title='Mapa distribución zona B&B')
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)

st.markdown("#### Descubre explorando:")
st.markdown("""
            - Más del 60 % de las celebridades se concentran en las tres áreas centrales de Tokyo, el distrito de 'Shibuya Ku', 'Sumida Ku' y 'Nerima Ku'.
            - Para las áreas alrededor del distrito de  'Shibuya Ku', 'Sumida Ku' y 'Nerima Ku', la distribución de casas de familia también está cerca de los límites de estas tres áreas, especialmente 'Setagaya Ku' y 'Arakawa Ku'.
            - Las áreas restantes están distribuidas de manera relativamente uniforme y no hay un centro obvio.
            """)
st.markdown("#### A continuación, continuaremos observando si el precio de las habitaciones en diferentes áreas será diferente")
st.markdown("#### Para evitar la interferencia de algunos valores atípicos, verifiquemos la distribución de precios antes de realizar un procesamiento razonable")

sns.histplot(datos['price'],color='b')
st.pyplot()
st.markdown("#### Consulta los precios en cada región")

a = datos[['neighbourhood','price']].groupby(['neighbourhood','price']).count().reset_index()
for i in names:
    plt.hist(a[a['neighbourhood']==i].price)
    plt.xlabel(i)
    # st.pyplot()
b = pd.DataFrame(datos['neighbourhood'].unique(),columns=['área'])
b['precio alto'] = datos[['price','neighbourhood']].groupby('neighbourhood').max().price.tolist()
b['precio bajo'] = datos[['price','neighbourhood']].groupby('neighbourhood').min().price.tolist()
b['precio mediano'] = datos[['price','neighbourhood']].groupby('neighbourhood').median().price.tolist()
b['25% de precio'] = datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.25).price.tolist()
b['75% de precio'] = datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.75).price.tolist()
b['cuartil'] = np.array(datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.75).price.tolist()) - np.array(datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.25).price.tolist())
st.write(b)
b['precio mediano'].max()
st.markdown("#### Del análisis anterior, se puede concluir que")
st.markdown("""
            - El precio de las casas de familia en Shinagawa Ku es generalmente el más alto (89955.0), seguido de Katsushika Ku (50035.0), y el tercero es Hinohara Mura (28460.5), y los precios de estas tres áreas están ampliamente distribuidos.
            - Sumida Ku, Shibuya Ku y Katsushika Ku, que tienen la mayor cantidad de casas de familia, tienen un precio de alrededor de 7.000, lo que explica en cierta medida la razón de la gran cantidad de casas de familia en la región.
            - Hay una gran diferencia entre el precio más alto y el precio más bajo en cada área, y el precio más alto en algunas áreas supera el millón de yuanes. No está claro si es un valor anormal o si el precio de la casa de familia en sí es tan alto. puede analizarse más a fondo en el área de grandes conjuntos de datos.
            """)
st.markdown("#### Airbnb")
st.markdown("""
            - top10 más populares
            - ¿Por qué es el más popular?
            """)
st.markdown("#### Aquí, por el momento, creemos que una reseña representa a un huésped, y aquellos con una reseña promedio/revisión mensual superior al 75 % de los dígitos son los B&B más populares.")
avg_review = datos['number_of_reviews'].quantile(0.9)
avg_month_review = datos['reviews_per_month'].quantile(0.9)
print(avg_review)
print(avg_month_review)
popular_house = datos[(datos['number_of_reviews']>avg_review) & (datos['reviews_per_month']>avg_month_review)]
st.write(popular_house.sort_values(by=['number_of_reviews','reviews_per_month'],ascending=False).head(10))
st.markdown("### La mayoría de las casas de familia más populares están en Shinjuku Ku (4 casas), algunas están en Katsushika Ku y Katsushika Ku y Taito Ku (2 cada una).")
st.markdown("### Las 10 casas de familia más populares son Entire. Se considera temporalmente que si desea hacer casas de familia, el Entire puede ser una buena opción.")
