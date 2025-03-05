import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st # type: ignore
from datetime import datetime
import folium # type: ignore
from streamlit_folium import folium_static # type: ignore
from folium.plugins import HeatMap # type: ignore

# Konfigurasi Style
sns.set(style='darkgrid')

# Load Data
df = pd.read_csv("all_data.csv")

# Konversi Kolom ke Format Datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# Sidebar untuk Rentang Tanggal
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")  # Ganti dengan logo jika ada
    start_date, end_date = st.date_input("Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter Data Berdasarkan Rentang Tanggal
main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

# Judul Dashboard
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis data peminjaman sepeda berdasarkan berbagai faktor.")

# -- VISUALISASI 1: Tren Jumlah Peminjaman Sepeda Sepanjang Waktu --
st.subheader("1. Tren Jumlah Peminjaman Sepeda Sepanjang Waktu")

daily_df = main_df.groupby("dteday")["cnt_day"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="dteday", y="cnt_day", data=daily_df, marker="o", color="#90CAF9", linewidth=2, ax=ax)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
ax.set_title("Tren Jumlah Peminjaman Sepeda Sepanjang Waktu", fontsize=14)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Jumlah peminjaman sepeda menunjukkan fluktuasi yang jelas sepanjang waktu, dengan pola musiman yang terlihat.")

# -- VISUALISASI 2: Pengaruh Faktor Cuaca terhadap Peminjaman --
st.subheader("2. Pengaruh Faktor Cuaca terhadap Peminjaman Sepeda")

weather_resampled = main_df.resample('M', on='dteday').agg({
    'temp_day': 'mean',
    'hum_day': 'mean',
    'windspeed_day': 'mean',
    'cnt_day': 'sum'
}).reset_index()

# Mengubah format tanggal
weather_resampled['dteday'] = weather_resampled['dteday'].dt.strftime('%Y-%m')

# Visualisasi Suhu vs Jumlah Peminjaman
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=weather_resampled, x='dteday', y='temp_day', label='Suhu (°C)', color='r')
sns.lineplot(data=weather_resampled, x='dteday', y='cnt_day', label='Total Peminjaman', color='b')
plt.xticks(rotation=45)
plt.title('Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda', fontsize=14)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Suhu / Jumlah Peminjaman', fontsize=12)
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Semakin tinggi suhu, semakin banyak sepeda yang dipinjam. Namun, pada suhu ekstrem, peminjaman cenderung berkurang.")

# Visualisasi Kelembaban vs Jumlah Peminjaman
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=weather_resampled, x='dteday', y='hum_day', label='Kelembaban (%)', color='g')
sns.lineplot(data=weather_resampled, x='dteday', y='cnt_day', label='Total Peminjaman', color='b')
plt.xticks(rotation=45)
plt.title('Pengaruh Kelembaban terhadap Jumlah Peminjaman Sepeda', fontsize=14)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Kelembaban / Jumlah Peminjaman', fontsize=12)
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Kelembaban yang tinggi dapat mempengaruhi minat pengguna untuk menyewa sepeda.")

# Visualisasi Kecepatan Angin vs Jumlah Peminjaman
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=weather_resampled, x='dteday', y='windspeed_day', label='Kecepatan Angin (m/s)', color='c')
sns.lineplot(data=weather_resampled, x='dteday', y='cnt_day', label='Total Peminjaman', color='b')
plt.xticks(rotation=45)
plt.title('Pengaruh Kecepatan Angin terhadap Jumlah Peminjaman Sepeda', fontsize=14)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Kecepatan Angin / Jumlah Peminjaman', fontsize=12)
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Kecepatan angin yang tinggi dapat mengurangi jumlah peminjaman sepeda, karena kondisi berkendara menjadi lebih sulit.")

# -- VISUALISASI 3: Perbedaan Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan --
st.subheader("3. Perbedaan Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan")

workingday_resampled = main_df.resample('W', on='dteday').agg({
    'cnt_day': 'sum',
    'workingday_day': 'mean'  # Rata-rata hari kerja dalam seminggu (0 = akhir pekan, 1 = hari kerja)
}).reset_index()

# Menghitung rata-rata peminjaman untuk hari kerja dan akhir pekan
avg_rentals = workingday_resampled.groupby('workingday_day')['cnt_day'].mean().reset_index()
avg_rentals['workingday_day'] = avg_rentals['workingday_day'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_rentals, x='workingday_day', y='cnt_day', palette='coolwarm', ax=ax)
plt.title('Rata-rata Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan', fontsize=14)
plt.xlabel('Hari Kerja', fontsize=12)
plt.ylabel('Rata-rata Total Peminjaman', fontsize=12)
plt.grid(axis='y')
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Lebih banyak sepeda dipinjam pada hari kerja dibandingkan akhir pekan, menunjukkan bahwa banyak orang menggunakan sepeda untuk keperluan transportasi.")

# -- VISUALISASI 4: Penggunaan Sepeda Berdasarkan Jam --
st.subheader("4. Penggunaan Sepeda Berdasarkan Jam")

hourly_resampled = main_df.groupby(['hr', 'season_hour']).agg({
    'casual_hour': 'sum',
    'registered_hour': 'sum',
    'cnt_hour': 'sum'
}).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_resampled, x='hr', y='cnt_hour', label='Total Peminjaman', color='b')
sns.lineplot(data=hourly_resampled, x='hr', y='casual_hour', label='Pengguna Kasual', color='g')
sns.lineplot(data=hourly_resampled, x='hr', y='registered_hour', label='Pengguna Terdaftar', color='r')
plt.title('Penggunaan Sepeda Berdasarkan Jam', fontsize=14)
plt.xlabel('Jam', fontsize=12)
plt.ylabel('Jumlah Peminjaman', fontsize=12)
plt.xticks(range(0, 24))
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Penggunaan sepeda mencapai puncaknya pada jam sibuk, terutama di pagi dan sore hari.")

# -- VISUALISASI 5: Pola Penggunaan Sepeda Berdasarkan Musim --
st.subheader("Pola Penggunaan Sepeda Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=hourly_resampled, x='season_hour', y='cnt_hour', palette='Set2', ax=ax)
plt.title('Pola Penggunaan Sepeda Berdasarkan Musim', fontsize=14)
plt.xlabel('Musim', fontsize=12)
plt.ylabel('Jumlah Peminjaman', fontsize=12)
plt.xticks(ticks=[0, 1, 2, 3], labels=['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])
plt.grid(axis='y')
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Musim panas menunjukkan tingkat peminjaman tertinggi, sedangkan musim dingin memiliki tingkat peminjaman terendah.")

# -- GEOSPASIAL ANALISYS --
st.subheader("Geospatial Analysis: Sebaran Peminjaman Sepeda")

# Menampilkan 5 lokasi dengan jumlah peminjaman tertinggi
top_locations = main_df.groupby(["latitude", "longitude"]).agg({"cnt_day": "sum"}).reset_index()
top_locations = top_locations.sort_values(by="cnt_day", ascending=False).head(5)
st.write("**Top 5 Lokasi dengan Peminjaman Terbanyak**")
st.dataframe(top_locations)

# Membuat Peta Interaktif dengan Folium
m = folium.Map(location=[top_locations["latitude"].mean(), top_locations["longitude"].mean()], zoom_start=12)

# Menambahkan titik lokasi sepeda berdasarkan jumlah peminjaman
for _, row in top_locations.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"Peminjaman: {row['cnt_day']} unit",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# Menampilkan Peta di Streamlit
st.write("**Peta Lokasi Peminjaman Sepeda**")
folium_static(m)

# Membuat Heatmap untuk melihat pola peminjaman
st.write("**Heatmap Peminjaman Sepeda**")
heatmap_data = main_df[["latitude", "longitude", "cnt_day"]].dropna()
heatmap_map = folium.Map(location=[heatmap_data["latitude"].mean(), heatmap_data["longitude"].mean()], zoom_start=12)
HeatMap(heatmap_data.values, radius=15).add_to(heatmap_map)

# Menampilkan Heatmap di Streamlit
folium_static(heatmap_map)

#terakhir
st.caption("Copyright (c) 2025 - Bike Sharing Dashboard by [Margohan] 🚲")
