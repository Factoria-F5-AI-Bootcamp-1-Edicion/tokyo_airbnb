import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Mi primero app de Streamlit Análisis y visualización de datos de Tokyo_Airbnb")
st.sidebar.image("pngkey.com-airbnb-logo-png-605967.png",width=72)

datos = pd.read_csv('tokyo_airbnb.csv')
datos['host_name'].fillna("0",inplace = True)
datos['last_review'].fillna('2018-01-01',inplace = True)
datos['last_review'] = pd.to_datetime(datos['last_review'],format='%Y-%m-%d')
datos['reviews_per_month'].fillna(0,inplace = True)
datos = datos.drop(columns='neighbourhood_group')

st.sidebar.write("1. La tabla de datos")
st.subheader(" 1. Después de limpiar datos ,La tabla se muestra")
datos

st.sidebar.write("2. Tipos de habitaciones")
st.subheader(" 2. Hay tres tipos de habitaciones en total: Private room, Entire home/apt y Shared room.")
st.write(" El análisis de las salas muestra que la mayoría de ellas se alquilan en conjunto, y pocas salas públicas se alquilan.")
plt.subplot(311)
data = datos['room_type'].value_counts().tolist()
a = datos['room_type'].unique()
plt.bar(x=a, height=data, color=['aquamarine', 'dodgerblue', 'deepskyblue'])
st.pyplot()

st.sidebar.write("3. ¿El último comentario comenzó en...?")
start_time = st.sidebar.slider(
     "¿El último comentario comenzó en...?",
     min_value = datetime(2018, 1, 1),
     max_value = datetime(2020, 1, 1),
     value = datetime(2018, 1, 2),
     format="MM/DD/YY")
st.sidebar.write(start_time)
if start_time != datetime(2018, 1, 2):
    if datos.loc[datos['last_review']==start_time].empty:
        st.subheader(f" 3. Pobrecito, no hay comentarios en este día {start_time}😭")
    else:
        st.subheader(f" 3. Todos los comentarios del día {start_time}")
        st.write(datos.loc[datos['last_review']==start_time])

st.sidebar.write("4. Análisis por host_name")
st.subheader(" 4. Se puede ver que host_name está relativamente concentrado, lo que puede confirmar la conclusión extraída en las listas de host_calculadas en el tipo continuo anterior.Vamos a verlo en detalle.")
arr = datos[['host_name','name']].groupby('host_name').count().sort_values(by='name', ascending=False)
st.line_chart(arr)

st.sidebar.write("5. Tokyo Alojamiento Mapa")
st.subheader("5. Tokyo Alojamiento Mapa")
map_data = pd.DataFrame(datos,columns=['latitude', 'longitude'])
st.map(map_data)

st.sidebar.write("6. Mapa distribución zona B&B")
st.subheader("5. Mapa distribución zona B&B")
values = datos.neighbourhood.value_counts()
names = datos.neighbourhood.unique().tolist()
fig = px.pie(datos, values=values, names=names)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)

st.subheader("Descubre explorando:")
st.markdown("""
            - Más del 40 % de las celebridades se concentran en las tres áreas centrales de Tokyo, el distrito de 'Shibuya Ku', 'Sumida Ku' y 'Nerima Ku'.
            - Para las áreas alrededor del distrito de  'Shibuya Ku', 'Sumida Ku' y 'Nerima Ku', la distribución de casas de familia también está cerca de los límites de estas tres áreas, especialmente 'Setagaya Ku' y 'Arakawa Ku'.
            - Las áreas restantes están distribuidas de manera relativamente uniforme y no hay un centro obvio.
            """)

st.sidebar.write("7. Análisis por price")
st.subheader(" 7. A continuación, continuaremos observando si el precio de las habitaciones en diferentes áreas será diferente")
sns.histplot(datos['price'],color='b')
st.pyplot()

st.sidebar.write("8. Consulta los precios en cada región")
st.subheader(" 8. Consulta los precios en cada región")
a = datos[['neighbourhood','price']].groupby(['neighbourhood','price']).count().reset_index()
option = st.sidebar.selectbox(
'¿En qué región le gustaría ver un histograma de "Área -- Precios"?',names)
plt.hist(a[a['neighbourhood']==option].price,color='pink')
plt.ylabel("precios")
plt.xlabel(option)
st.pyplot() 

st.sidebar.write("9. Categorizar precios")
st.subheader(" 9. Categorizar precios")
b = pd.DataFrame(datos['neighbourhood'].unique(),columns=['área'])
b['precio alto'] = datos[['price','neighbourhood']].groupby('neighbourhood').max().price.tolist()
b['precio bajo'] = datos[['price','neighbourhood']].groupby('neighbourhood').min().price.tolist()
b['precio mediano'] = datos[['price','neighbourhood']].groupby('neighbourhood').median().price.tolist()
b['25% de precio'] = datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.25).price.tolist()
b['75% de precio'] = datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.75).price.tolist()
b['cuartil'] = np.array(datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.75).price.tolist()) - np.array(datos[['price','neighbourhood']].groupby('neighbourhood').quantile(0.25).price.tolist())
st.write(b)
b['precio mediano'].max()

st.sidebar.write("10. topc 10 más populares Airbnb")
st.subheader(" 10. top 10 más populares Airbnb")
avg_review = datos['number_of_reviews'].quantile(0.9)
avg_month_review = datos['reviews_per_month'].quantile(0.9)
print(avg_review)
print(avg_month_review)
popular_house = datos[(datos['number_of_reviews']>avg_review) & (datos['reviews_per_month']>avg_month_review)]
st.write(popular_house.sort_values(by=['number_of_reviews','reviews_per_month'],ascending=False).head(10))
st.write(" La mayoría de las casas de familia más populares están en Shinjuku Ku (4 casas), algunas están en Katsushika Ku y Katsushika Ku y Taito Ku (2 cada una).")
st.write(" Las 10 casas de familia más populares son Entire. Se considera temporalmente que si desea hacer casas de familia, el Entire puede ser una buena opción.")


if st.sidebar.button('gracias'):
    st.balloons()
else:
    st.write(' gracias a todos!!!')
