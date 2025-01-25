# 📊 Proyek Analisis Kualitas Udara

Dashboard interaktif untuk memantau kualitas udara dari 12 stasiun pemantauan (2013-2017).

## 🚀 Cara Menjalankan

### Prasyarat:
- Python 3.9+
- Git (opsional)

### Langkah 1: Clone Repositori
```bash
git clone https://github.com/luckelis/air-quality-dashboard
cd analisis-kualitas-udara/dashboard
```

### Langkah 2: Instal Dependensi
```bash
pip install -r requirements.txt
```

### Langkah 3: Jalankan Dashboard
```bash
streamlit run app.py
```

### Struktur Folder
```
analisis-kualitas-udara/
├── dashboard/
│   ├── app.py
│   ├── cleaned_air_quality_data.csv
│   └── requirements.txt
├── data/
│   └── (file-data-mentah) 
└── notebooks/
    └── analysis.ipynb
```

## 🛠️ Troubleshooting
1. **File CSV Tidak Ditemukan**:
   - Pastikan file `cleaned_air_quality_data.csv` ada di folder `dashboard`.
   - Periksa penulisan nama file (case-sensitive).

2. **Error Dependensi**:
   - Update pip: `pip install --upgrade pip`
   - Instal ulang requirements: `pip install -r requirements.txt`

3. **Port Terblokir**:
   - Gunakan port alternatif:  
     ```bash
     streamlit run app.py --server.port 8502
     ```

## 📊 Fitur Dashboard
- Analisis spasial per stasiun
- Tren temporal polutan (PM2.5, PM10, dll.)
- Filter interaktif berdasarkan waktu dan lokasi

## 📧 Kontribusi
Dikembangkan oleh [Nama Anda] - [email@contoh.com]