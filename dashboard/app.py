import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import requests  

# Load dataset
@st.cache_data(persist=True)
def load_data():
    try:
        df = pd.read_csv("main_data.csv", encoding="latin-1")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

# Muat Data 
df = load_data()

if df is None:
    st.error("Data tidak dapat dimuat!. Periksa file main_data.csv dan encodingnya.")
    st.stop()

# Pastikan kolom 'order_approved_at' adalah datetime
df["order_approved_at"] = pd.to_datetime(df["order_approved_at"], errors="coerce")

# Judul
st.title("Dashboard Analisis E-Commerce")
st.write(f"Dataset memuat **{df.shape[0]} baris** dan **{df.shape[1]} kolom**.")
st.write("---")

# Sidebar
st.sidebar.header("Filter")
selected_state = st.sidebar.selectbox("Pilih Negara Bagian:", df["customer_state"].dropna().unique())

# Filter Waktu (Slider)
start_date, end_date = st.sidebar.slider(
    "Pilih Rentang Tanggal", 
    min_value=df["order_approved_at"].min().date(),  # Pastikan menjadi tanggal (datetime.date)
    max_value=df["order_approved_at"].max().date(),  # Pastikan menjadi tanggal (datetime.date)
    value=(df["order_approved_at"].min().date(), df["order_approved_at"].max().date()),  # Default range
    format="YYYY-MM-DD"
)

# Filter Data Berdasarkan Tanggal dan Negara Bagian
filtered_df = df[(df["customer_state"] == selected_state) &  # Pastikan ada & di sini
                 (df["order_approved_at"].dt.date >= start_date) &  # Pastikan menggunakan & untuk kondisi
                 (df["order_approved_at"].dt.date <= end_date)]  # Menambahkan & di sini


# Filtered Data
st.write(f"Data terfilter dengan **{filtered_df.shape[0]} baris** berdasarkan negara bagian **{selected_state}**, tanggal, dan kota pelanggan.")

# Layout
st.subheader(f"Jumlah Pelanggan dan Penjual di {selected_state}")
col1, col2 = st.columns(2)

with col1:
    customer_counts = filtered_df["customer_state"].value_counts()
    st.metric(label="Jumlah Pelanggan", value=customer_counts.sum())

with col2:
    seller_counts = filtered_df["seller_state"].value_counts()
    st.metric(label="Jumlah Penjual", value=seller_counts.sum())


# Analisis Pertanyaan 1: Jumlah Pelanggan dan Penjual
st.subheader(f"Jumlah Pelanggan & Penjual di {selected_state}")
fig, ax = plt.subplots(figsize=(10, 5))
customer_counts.plot(kind="bar", color='blue', alpha=0.7, label='Pelanggan', ax=ax)
seller_counts.plot(kind="bar", color='red', alpha=0.7, label='Penjual', ax=ax)
ax.set_xlabel("Negara Bagian")
ax.set_ylabel("Jumlah")
ax.set_title(f"Jumlah Pelanggan & Penjual di {selected_state}")
ax.legend()
st.pyplot(fig)

# Insight Analisis Pertanyaan 1
st.markdown(
    f"**Insight Analisis Pertanyaan 1 :** Di {selected_state}, perbandingan jumlah pelanggan dan penjual menunjukkan \"{'lebih banyak penjual daripada pelanggan' if seller_counts.sum() > customer_counts.sum() else 'lebih banyak pelanggan daripada penjual'}\"."
)

# Analisis Pertanyaan 2: Distribusi Status Pesanan
st.subheader("Distribusi Status Pesanan")
status_counts_filtered = filtered_df["order_status"].value_counts()
fig2, ax2 = plt.subplots()
sns.barplot(x=status_counts_filtered.index, y=status_counts_filtered.values, palette='viridis', ax=ax2)
ax2.set_xlabel("Status Pesanan")
ax2.set_ylabel("Jumlah Pesanan")
st.pyplot(fig2)

st.write("---")

# Insight Analisis Pertanyaan 2
total_orders = status_counts_filtered.sum()
most_common = status_counts_filtered.idxmax()
percentage = status_counts_filtered.max() / total_orders * 100
st.markdown(
    f"**Insight Analisis Pertanyaan 2 :** Dari total {total_orders:,} pesanan, status **{most_common}** mendominasi sekitar {percentage:.1f}% dari keseluruhan."
)

# Pastikan kolom 'order_approved_at' adalah datetime
filtered_df["order_approved_at"] = pd.to_datetime(filtered_df["order_approved_at"], errors="coerce")

# Analisis Pertanyaan 3: Pola transaksi harian berdasarkan pesanan yang disetujui
st.subheader("Pola Transaksi Harian")
filtered_df["order_approved_at"] = pd.to_datetime(filtered_df["order_approved_at"], errors='coerce')
daily_orders = filtered_df.groupby(filtered_df["order_approved_at"].dt.date).size()
st.line_chart(daily_orders)
st.write("---")

# Insight Analisis Pertanyaan 3
peak_date = daily_orders.idxmax()
peak_value = daily_orders.max()
avg_orders = daily_orders.mean()
st.markdown(
    f"**Insight Analisis Pertanyaan 3 :** Puncak transaksi harian terjadi pada **{peak_date}** dengan {peak_value} pesanan. Rata-rata transaksi harian adalah sekitar {avg_orders:.0f} pesanan."
)


# Peta distribusi pesanan per negara bagian
st.subheader("Peta Distribusi Pesanan per Negara Bagian")
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

# Mengunduh file GeoJSON
geojson_data = requests.get(geojson_url).json()

# Menyiapkan data untuk peta
state_order_counts = filtered_df['customer_state'].value_counts().reset_index()
state_order_counts.columns = ['State', 'Order_Count']

# Membuat choropleth map
fig_geo = px.choropleth(state_order_counts, 
                        locations='State', 
                        locationmode="geojson-id", 
                        color='Order_Count',
                        geojson=geojson_data,
                        featureidkey="properties.sigla", 
                        title="Distribusi Pesanan E-Commerce per Negara Bagian di Brazil")

# Mengupdate peta
fig_geo.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_geo)

# Insight setelah peta
top_states = state_order_counts.sort_values(by='Order_Count', ascending=False).head(5)
bottom_states = state_order_counts.sort_values(by='Order_Count').head(5)


st.write("---")
st.markdown("""
**Insight Peta Distribusi Pesanan:**
1. **Negara Bagian dengan Pesanan Terbanyak**:
    - Negara bagian **São Paulo (SP)** memiliki jumlah pesanan terbanyak, menunjukkan konsentrasi tinggi dalam aktivitas e-commerce. Hal ini mungkin dipengaruhi oleh kepadatan penduduk dan infrastruktur yang lebih maju di wilayah tersebut.
    
2. **Negara Bagian dengan Pesanan Paling Sedikit**:
    - Negara bagian **Roraima (RR)** dan **Acre (AC)** menunjukkan angka pesanan yang rendah. Ini bisa menunjukkan tantangan logistik atau rendahnya penetrasi e-commerce di wilayah tersebut.

3. **Ketimpangan Distribusi**:
    - Peta ini menunjukkan ketimpangan dalam distribusi pesanan, di mana sebagian besar aktivitas e-commerce terkonsentrasi di negara bagian seperti **São Paulo**, sementara banyak negara bagian lain memiliki lebih sedikit pesanan.
""")


# Menutup aplikasi
st.write("---")
st.write("Dashboard ini dibuat oleh Farah Putri Firdausa A278XAF155")
