import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

############## FUNCTION ##############


def create_byseason_df(df):
    season_dict = {
        1: "Winter",
        2: "Spring",
        3: "Summer",
        4: "Fall"
    }

    df_bike['season_name'] = df_bike['season'].map(season_dict)

    df_season = df_bike.groupby('season_name').agg({
        'cnt': 'sum'
    }).reset_index()

    df_season.rename(columns={
        'cnt': 'user_count'
    }, inplace=True)

    return df_season


def create_byweather_df(df):
    weather_dict = {
        1: "Mostly clear",
        2: "Mist clouds",
        3: "Light rain/snow",
        4: "Heavy rain/snow"
    }

    df_bike['weather_name'] = df_bike['weathersit'].map(weather_dict)

    df_weather = df_bike.groupby('weather_name').agg({
        'cnt': 'sum'
    }).reset_index()

    df_weather.rename(columns={
        'cnt': 'user_count'
    }, inplace=True)

    return df_weather


def create_byworkingday_df(df):
    df_workingday = df_bike.groupby('workingday').agg({
        'cnt': 'sum'
    }).reset_index()

    df_workingday.rename(columns={
        'instant': 'user_count'
    }, inplace=True)

    return df_workingday


def create_byhour_df(df):
    df_bike_hr = df_bike.groupby('hr').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False).reset_index()

    return df_bike_hr

############## END FUNCTION ##############


df_bike = pd.read_csv("./hour.csv")

datetime_columns = ["dteday"]
df_bike.sort_values(by="dteday", inplace=True)
df_bike.reset_index(inplace=True)

for column in datetime_columns:
    df_bike[column] = pd.to_datetime(df_bike[column])

min_date = df_bike['dteday'].min()
max_date = df_bike['dteday'].max()

with st.sidebar:
    st.image(
        'https://images.squarespace-cdn.com/content/60db56245562a41693c7c918/127f61f2-f977-4ac0-8a8d-c8279b4eada8/hhbr_2022.png?format=1500w&content-type=image%2Fpng')

    start_date, end_date = st.date_input(
        label='Date Range', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    st.subheader('About Dataset')
    st.markdown('''
                Bike sharing systems are new generation of traditional 
                bike rentals where whole process from membership, 
                rental and return back has become automatic. 
                Through these systems, user is able to easily rent a bike 
                from a particular position and return back at another position.''')

main_df = df_bike[(df_bike["dteday"] >= str(start_date)) &
                  (df_bike["dteday"] <= str(end_date))]


df_season = create_byseason_df(main_df)
df_weather = create_byweather_df(main_df)
df_workingday = create_byworkingday_df(main_df)
df_bike_hr = create_byhour_df(main_df)

####################### TITLE  #######################
st.title('Dashboard Bike Rental Systems🚲')
####################### CUSTOMER DEMOGRAPHICS #######################
st.header("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    colors = ['#7AE582', '#D3D3D3', '#D3D3D3', '#D3D3D3']

    fig = plt.figure(figsize=(10, 5))
    sns.barplot(
        y="user_count",
        x='season_name',
        data=df_season.sort_values(by='user_count', ascending=False),
        palette=colors
    )

    plt.title("Number of Customer by Season", loc='center', fontsize=15)
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(fig)

with col2:
    colors = ['#7AE582', '#D3D3D3', '#D3D3D3']
    fig = plt.figure(figsize=(10, 5))
    sns.barplot(
        y="user_count",
        x='weather_name',
        data=df_weather.sort_values(by='user_count', ascending=False),
        palette=colors
    )

    plt.title("Number of Customer by Weather Condition",
              loc='center', fontsize=15)
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15, 8))

colors_2 = ['#98c9a3', '#ffc9b9', '#bc4b51', '#fbb02d']
sns.barplot(data=df_bike, x='workingday', y='cnt',
            hue='season_name', palette=colors_2)
plt.title('Workingday Based on Season Distribution', loc='center', fontsize=15)
plt.ylabel(None)
st.pyplot(fig)

####################### MOST AND LESS RENTAL BIKE HOURS  #######################
st.header("Most and Less Rental Bike Hours")

col1, col2 = st.columns(2)

with col1:
    most_hour = df_bike_hr['hr'][0]
    st.metric("Most Hours", value=most_hour)

with col2:
    fewer_hour = df_bike_hr['hr'][23]
    st.metric("Fewer Hours", value=fewer_hour)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ['#7AE582', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3']
colors_2 = ['#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#7AE582']

sns.barplot(x="hr", y="cnt", data=df_bike_hr.sort_values(
    by="hr", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most Rental Bike Hours", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="hr", y="cnt", data=df_bike_hr.sort_values(
    by="hr", ascending=True).head(5), palette=colors_2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Less Rental Bike Hours", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle("Most and Less Rental Bike Hours", fontsize=20)
st.pyplot(fig)

st.subheader('Conclusion')
st.markdown('''
**1. Bagaimana demografi pengguna sepeda?**
- Berdasarkan visualisasi di atas demografi pelanggan berdasarkan season, pelanggan yang menyewa sepeda lebih banyak pada musim panas (Summer) dan paling sedikit pada musim salju (Winter).
- Berdasarkan Weather Condition atau sistuasi cuaca, banyak pelanggan menyewa sepeda pada cuaca cerah (Mostly Clear) dan sedikit pada cuaca hujan atau salju (Heavy Rain/Snow).
- Berdasarkan Working day atau hari kerja dan seasonnya, banyak pelanggan menyewa sepeda pada musim panas di hari kerja (bernilai 1) dibandingkan hari libur.

**2. Pada jam berapa paling banyak dan sedikit pengguna menyewa sepeda?**
- Pengguna menyewa sepeda paling banyak pada jam 17 diikuti jam 18. 
- Paling sedikit pada jam 4 pagi diikuti jam 3 pagi.
''')
