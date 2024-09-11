import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import plotly.express as px
from plotly.subplots import make_subplots
sns.set(style='dark')

# 1. Ghatering Data
day_df=pd.read_csv("day_final.csv", delimiter=",")
hour_df=pd.read_csv("hour_final.csv", delimiter=";")

# 2. Cleaning Data
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
str_column = ["season", "yr", "mnth", "holiday", "weekday", "workingday", "weathersit"]
for column in str_column:
  day_df[column] = day_df[column].astype('category')

hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
str_column = ["season", "yr", "mnth","holiday", "hr","weekday", "workingday", "weathersit"]
for column in str_column:
  hour_df[column] = hour_df[column].astype('category')

# 3. Helper Function Daily
def create_daily_rental_df(df):
  daily_rental_df = df.resample(rule = 'D', on="dteday").agg({
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum"
  })
  return daily_rental_df

# 4.1 Helper Function Season
def create_season_rental_df(df):
  season_rental_df = df.groupby(by='season').agg({ 
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum"
  })
  season_rental_df = season_rental_df.reset_index()
  return season_rental_df

# 4.2 Helper Function Weathersit
def create_weathersit_rental_df(df):
  weathersit_rental_df = df.groupby(by='weathersit').agg({
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum",
    "temp" : "mean",
    "atemp" : "mean",
    "hum" : "mean",
    "windspeed" : "mean"
    })
  weathersit_rental_df = weathersit_rental_df.reset_index()
  return weathersit_rental_df


# 5.1 Helper Functional weekday
def create_weekday_rental_df(df):
  weekday_rental_df = df.groupby(by='weekday').agg({
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum"
  })
  weekday_rental_df = weekday_rental_df.reset_index()
  return weekday_rental_df
# 5.2 Helper Functional workingday
def create_workingday_rental_df(df):
  workingday_rental_df = df.groupby(by='workingday').agg({
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum"
  })
  workingday_rental_df = workingday_rental_df.reset_index()
  return workingday_rental_df

# 6. Helper Functional Hour
def create_hourly_rental_df(df):
  hourly_rental_df = df.groupby(by='hr').agg({
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum",
    "temp" : "mean",
    "atemp" : "mean",
    "hum" : "mean",
    "windspeed" : "mean"
  })
  hourly_rental_df = hourly_rental_df.reset_index()
  return hourly_rental_df

# 7. Helper Function Hourly and daily
def create_dailyhour_rental_df(df):
   daily_hourly_rental_df=df.groupby(by=['weekday','hr']).agg({
    "casual": "sum",
    "registered": "sum",
    "cnt":"sum",
    "temp":"mean",
    "atemp":"mean",
    "hum":"mean",
    "windspeed":"mean"
    })
   daily_hourly_rental_df = daily_hourly_rental_df.reset_index()
   return daily_hourly_rental_df

# Make Component Filter
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:

  st.title("Bike Sharing dataset")
  title_alignment="""
<style>
#bike-sharing-datasets {
  text-align: center
}
</style>
  """
  st.markdown(title_alignment, unsafe_allow_html=True)
  # Membuat logo perusahaan
  left_co, cent_co,last_co = st.columns(3)
  with cent_co:
    st.image ("https://cdn-icons-png.flaticon.com/128/1361/1361279.png")
  
  # Mengambil start_date & end_date dari date_input
  start_date, end_date = st.date_input(
    label = 'Rentang Waktu', min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
  )
main_df = day_df[(day_df["dteday"] >= str(start_date))&
                 (day_df["dteday"] <= str(end_date))]
hourly_df = hour_df[(hour_df["dteday"] >= str(start_date))&
                 (hour_df["dteday"] <= str(end_date))]

daily_rented_df = create_daily_rental_df(main_df)
season_rented_df = create_season_rental_df (main_df)
weathersit_rented_df = create_weathersit_rental_df (main_df)
weekday_rented_df = create_weekday_rental_df (main_df)
workingday_rented_df = create_workingday_rental_df (main_df)
hourly_rented_df = create_hourly_rental_df(hourly_df)
dailyhour_rented_df = create_dailyhour_rental_df (hourly_df)

st.header('Hasil Analisis Bike Sharing Dataset :Bike:')
tab1, tab2, tab3 , tab4, tab5 = st.tabs(["Conclusion Pertayaan 1", "Conclusion Pertayaan 2", "Conclusion Pertayaan 3","Conclusion Pertayaan 4", "Conclusion Pertayaan 5"])

with tab1:
    st.subheader('Pertayaan 1 : Melihat Tren Jumlah Pengguna Tahun 2011-2012?')
    daily_rented_df = create_daily_rental_df(main_df)
    st.write(daily_rented_df)
    col1, col2, col3, = st.columns(3)
    with col1:
      daily_rental_df_casual = round(daily_rented_df.casual.mean(),1)
      st.metric("Jumlah Pengguna Sepeda Casual Setiap Hari", value=daily_rental_df_casual)
    with col2:
      daily_rental_df_registered = round(daily_rented_df.registered.mean(),2)
      st.metric("Jumlah Pengguna Sepeda Registered Setiap Hari", value=daily_rental_df_registered)
    with col3:
      daily_rental_df_cnt = round(daily_rented_df.cnt.mean(),2)
      st.metric("Jumlah Pengguna Sepeda Cnt Setiap Hari", value= daily_rental_df_cnt)

    daily_rented_df_plot = daily_rented_df.reset_index()
    def show_daily_rental_df_by_category(df, x, columns, title, colors_theme):
       figure = px.line(daily_rented_df_plot, x=x, y=columns,
                  color_discrete_sequence=colors_theme,
              title=title
              )
       return figure

    x = 'dteday'
    columns = ['casual', 'registered', 'cnt']
    title = 'Jumlah Pengguna Sepeda Setiap Hari'
    colors_theme = ['red', 'yellow', 'green']
    st.plotly_chart( show_daily_rental_df_by_category(daily_rented_df, x, columns, title, colors_theme))

with tab2:
    st.subheader('Pertayaan 2 : Bagaimana Pola Penyewaan Sepeda Berdasarkan Musim dan Cuaca yang ada?')
    season_rented_df = create_season_rental_df (main_df)
    st.write(season_rented_df)

    season_rented_df_plot = season_rented_df.reset_index()
    def show_season_rented_df_by_category(df, x, columns, title, colors_theme):
       figure = px.bar(season_rented_df_plot, x=x, y=columns,
                  color_discrete_sequence=colors_theme, barmode='group',
              title=title
              )
       return figure
    x = 'season'
    columns = ['casual', 'registered', 'cnt']
    title = 'Jumlah Pengguna Sepeda di Setiap Musim'
    colors_theme = [ 'blueviolet', 'forestgreen', 'blue']
    st.plotly_chart(show_season_rented_df_by_category(season_rented_df , x, columns, title, colors_theme))

    weathersit_rented_df = create_weathersit_rental_df (main_df)
    st.write( weathersit_rented_df)
    weathersit_rented_df_plot = weathersit_rented_df.reset_index()
    def show_weathersit_rented_df_by_category(df, x, columns, title, colors_theme):
       figure = px.bar(weathersit_rented_df_plot, x=x, y=columns,
                  color_discrete_sequence=colors_theme, barmode='group',
              title=title
              )
       return figure
    x = 'weathersit'
    columns = ['casual', 'registered', 'cnt']
    title = 'Jumlah Pengguna Sepeda di Setiap Cuaca yang terjadi'
    colors_theme = [ 'lavender', 'plum', 'fuchsia']
    st.plotly_chart(show_weathersit_rented_df_by_category(weathersit_rented_df , x, columns, title, colors_theme))
    
with tab3:
    st.subheader('Pertayaan 3 : Melihat perbandingan penyewaan sepeda menurut Hari dalam seminggu dan Hari Kerja?')
    weekday_rented_df = create_weekday_rental_df (main_df)
    st.write(weekday_rented_df)

    weekday_rented_df_plot = weekday_rented_df.reset_index()
    def show_weekday_rented_df_by_category(df, x, columns, title, colors_theme):
       figure = px.bar(weekday_rented_df_plot, x=x, y=columns,
                  color_discrete_sequence=colors_theme, barmode='group',
              title=title
              )
       return figure
    x = 'weekday'
    columns = ['casual', 'registered', 'cnt']
    title = 'Melihat penyewaan sepeda menurut Hari dalam seminggu'
    colors_theme = [ 'MidnightBlue', 'cornflowerBlue', 'PowderBlue']
    st.plotly_chart(show_weekday_rented_df_by_category(weekday_rented_df , x, columns, title, colors_theme))
    
    workingday_rented_df = create_workingday_rental_df (main_df)
    st.write(workingday_rented_df)

    workingday_rented_df_plot = workingday_rented_df.reset_index()
    def show_workingday_rented_df_by_category(df, x, columns, title, colors_theme):
       figure = px.bar(workingday_rented_df_plot, x=x, y=columns,
                  color_discrete_sequence=colors_theme, barmode='group',
              title=title
              )
       return figure
    x = 'workingday'
    columns = ['casual', 'registered', 'cnt'] 
    title = 'Melihat penyewaan sepeda menurut Hari Kerja'
    colors_theme = ['maroon', 'magenta', 'purple']
    st.plotly_chart(show_workingday_rented_df_by_category(workingday_rented_df , x, columns, title, colors_theme))

with tab4:
    st.subheader('Pertayaan 4 : Melihat Tren Jumlah Berdasarkan Jam?')
    hourly_rented_df = create_hourly_rental_df(hourly_df)
    st.write(hourly_rented_df)

    hourly_rented_df_plot = hourly_rented_df.reset_index() 
    def show_hourly_rented_df_by_category(df, x, columns, title, colors_theme):
       figure = px.line(hourly_rented_df_plot, x=x, y=columns,
                  color_discrete_sequence=colors_theme,
              title=title
              )
       return figure
    x = 'hr'
    columns = ['casual', 'registered', 'cnt']
    title = 'Melihat Tren Jumlah Berdasarkan Jam'
    colors_theme = ['red', 'yellow', 'green']
    st.plotly_chart(show_hourly_rented_df_by_category(hourly_rented_df, x, columns, title, colors_theme))

with tab5:
    st.subheader('Pertayaan 5 : Melihat Pengguna Sepeda Menurut Jam dan Hari?')
    dailyhour_rented_df = create_dailyhour_rental_df (hourly_df)
    st.write(dailyhour_rented_df )

    dailyhour_rented_df_plot = dailyhour_rented_df.reset_index()
    def show_dailyhour_rented_df_by_category(df, x, columns, title, colors_theme, facet_col=None, facet_col_wrap=None):
       figure = px.line(dailyhour_rented_df_plot, x=x, y=columns,
                  color_discrete_sequence=colors_theme,
                        title=title,
                        facet_col=facet_col,
                        facet_col_wrap=facet_col_wrap  
              )
       return figure
    x = 'hr'
    columns = ['casual', 'registered', 'cnt']
    title = 'Melihat Tren Jumlah Berdasarkan Jam dan Hari'
    colors_theme = ['orchid', 'darkred','blue']
    st.plotly_chart(show_dailyhour_rented_df_by_category(dailyhour_rented_df , x, columns, title, colors_theme,facet_col="weekday",facet_col_wrap=2))
      








 

    
