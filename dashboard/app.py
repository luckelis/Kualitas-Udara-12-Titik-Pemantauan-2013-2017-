# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

# Konfigurasi path absolut sesuai lokasi file Anda
DATA_PATH = r"C:\tomy\Etha\Analisa_kualitas_udara\dashboard\cleaned_air_quality_data.csv"

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Kualitas Udara",
    page_icon="🌫️",
    layout="wide"
)

@st.cache_data
def load_data():
    try:
        # Cek eksistensi file
        if not Path(DATA_PATH).exists():
            st.error(f"❌ File tidak ditemukan di lokasi:\n{DATA_PATH}")
            st.error("Pastikan:")
            st.markdown("""
            1. Nama file tepat: `cleaned_air_quality_data.csv`
            2. Path folder benar: `C:\\tomy\\Etha\\Analisa_kualitas_udara\\dashboard\\`
            3. File tidak sedang terbuka di program lain
            """)
            return None
            
        # Load data
        df = pd.read_csv(DATA_PATH)
        
        # Validasi kolom
        required_columns = ['No','year','month','day','hour','PM2.5','PM10','SO2','NO2','CO','O3','TEMP','PRES','DEWP','RAIN','wd','WSPM','station']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"Kolom yang hilang: {', '.join(missing_cols)}")
            return None
            
        # Buat kolom datetime
        df['datetime'] = pd.to_datetime(
            df['year'].astype(str) + '-' +
            df['month'].astype(str) + '-' +
            df['day'].astype(str) + ' ' +
            df['hour'].astype(str) + ':00:00'
        )
        
        # Konversi tipe data numerik
        numeric_cols = ['PM2.5','PM10','SO2','NO2','CO','O3','TEMP','PRES','DEWP','RAIN','WSPM']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        return df

    except Exception as e:
        st.error(f"🚨 Error saat memuat data: {str(e)}")
        return None

def main():
    st.title("🌍 Dashboard Kualitas Udara 12 Titik Pemantauan (2013-2017)")
    
    # Debugging info
    st.sidebar.markdown(f"**Path file data:** `{DATA_PATH}`")
    st.sidebar.markdown(f"**Status file:** {'✅ Ditemukan' if Path(DATA_PATH).exists() else '❌ Tidak Ditemukan'}")
    
    # Load data
    with st.spinner('Memuat data...'):
        df = load_data()
    
    if df is None:
        st.stop()

    # ========================
    # ANALISIS DATA
    # ========================
    
    # Filter stasiun
    selected_station = st.selectbox(
        "Pilih Stasiun Pemantauan",
        options=df['station'].unique(),
        index=0
    )
    
    # Filter data
    filtered_df = df[df['station'] == selected_station]
    
    # Tampilkan metrik utama
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rata-rata PM2.5", f"{filtered_df['PM2.5'].mean():.1f} µg/m³", "WHO Guideline: 25 µg/m³")
    with col2:
        st.metric("Rata-rata PM10 Tertinggi", f"{filtered_df['PM10'].mean():.1f} µg/m³")
    with col3:
        st.metric("Rata-rata O3 Maksimal", f"{filtered_df['O3'].mean():.1f} µg/m³")
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Rata-rata SO2 Maksimal", f"{filtered_df['SO2'].mean():.1f} µg/m³")
    with col5:
        st.metric("Rata-rata CO Maksimal", f"{filtered_df['CO'].mean():.1f} µg/m³")
    with col6:
        st.metric("Rata-rata NO2 Maksimal", f"{filtered_df['NO2'].mean():.1f} µg/m³")

        # ===== Analisis Temporal =====
    st.header("Analisis Temporal")
    
    # Pilih polutan
    selected_pollutant = st.selectbox(
        "Pilih Polutan",
        options=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    )
    
    try:
        # Filter data valid
        df_clean = df.dropna(subset=[selected_pollutant, 'datetime']).copy()
        
        # Resample data bulanan dengan aggregasi mean
        resampled = df_clean.resample('M', on='datetime')[selected_pollutant].mean().reset_index()
        
        # Filter tanggal sesuai range data asli
        min_date = df_clean['datetime'].min()
        max_date = df_clean['datetime'].max()
        resampled = resampled[
            (resampled['datetime'] >= min_date) & 
            (resampled['datetime'] <= max_date)
        ]

        # Buat plot dengan matplotlib untuk kontrol lebih baik
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot data
        ax.plot(
            resampled['datetime'],
            resampled[selected_pollutant],
            marker='o',
            linestyle='-',
            color='#1f77b4'
        )
        
        # Formatting plot
        ax.set_title(f'Tren {selected_pollutant} ({min_date.year}-{max_date.year})', fontsize=14)
        ax.set_xlabel('Tanggal', fontsize=12)
        ax.set_ylabel(f'Konsentrasi {selected_pollutant} (µg/m³)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format tanggal di x-axis
        fig.autofmt_xdate()
        
        # Set batas axis sesuai data
        ax.set_xlim([min_date, max_date])
        
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Gagal membuat grafik: {str(e)}")

# ... [Kode setelahnya tetap sama]

if __name__ == "__main__":
    main()