# Brazilian E-Commerce Data Analysis Dashboard

## Deskripsi
Dashboard ini melakukan **analisis data e-commerce** publik dari Brazil untuk menjawab beberapa **pertanyaan bisnis** utama:

- **Negara bagian mana di Brazil yang memiliki jumlah pelanggan dan penjual terbanyak?**
- **Bagaimana distribusi status pesanan di seluruh Brasil?**
- **Bagaimana pola transaksi harian selama periode tertentu?**

Dashboard ini menggunakan **Streamlit** untuk visualisasi interaktif dan memungkinkan pengguna untuk mengeksplorasi data berdasarkan **negara bagian**, **tanggal**, dan **kategori produk**.

## Struktur Folder
- **data/**: Berisi file CSV asli yang digunakan dalam analisis (`data1.csv`, `data2.csv`, `data3.csv`, `data4.csv`).
- **dashboard/**: Berisi file utama untuk aplikasi dashboard (`app.py`) dan file data gabungan (`main_data.csv`).
- **notebook.ipynb**: Notebook Jupyter yang digunakan untuk melakukan analisis data sebelum aplikasi dashboard.
- **requirements.txt**: Daftar dependensi yang digunakan dalam proyek ini.
- **url.txt**: URL untuk mengakses **Live Dashboard** di Streamlit Cloud.

## Cara Menjalankan Dashboard

### Menjalankan secara Lokal:
1. **Clone repo**:
   - Gunakan perintah berikut untuk meng-clone repository ini:
     ```bash
     git clone https://github.com/username/repository.git
     ```
2. **Instal dependensi**:
   - Jalankan perintah untuk menginstal semua dependensi yang dibutuhkan:
     ```bash
     pip install -r requirements.txt
     ```
3. **Jalankan aplikasi Streamlit**:
   - Setelah dependensi diinstal, jalankan aplikasi dengan perintah berikut:
     ```bash
     streamlit run dashboard/app.py
     ```

### Link Live App
Akses aplikasi **live dashboard** yang di-deploy menggunakan **Streamlit Cloud** melalui tautan berikut:

[Live Dashboard](https://ecommerce-dashboard-wawioxnt59wmatnlcqcas2.streamlit.app/)

## Fitur Dashboard:
1. **Filter Berdasarkan Negara Bagian dan Kategori Produk**: 
   - Pengguna dapat memilih negara bagian dan kategori produk untuk melakukan analisis yang lebih mendalam.
   
2. **Visualisasi Peta Distribusi Pesanan**: 
   - Peta interaktif menunjukkan distribusi pesanan berdasarkan negara bagian di Brazil.

3. **Grafik Analisis Status Pesanan dan Pola Transaksi Harian**: 
   - Memvisualisasikan status pesanan dan tren transaksi harian selama periode yang dipilih.

## Catatan
- Pastikan **`main_data.csv`** sudah tersedia di folder **`dashboard/`** sebelum menjalankan aplikasi.
