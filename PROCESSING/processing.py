import pandas as pd
import numpy as np

# Load data warga
df = pd.read_excel('../DATASET/dataset.xlsx')

# Bobot masing-masing kriteria (total = 1.0)
weights = {
    'Pekerjaan': 0.4,
    'DTKS': 0.2,
    'PKH': 0.3,
    'Kartu Pra Kerja': 0.1,
    'BST' : 0.1,
    'Bansos Pemerintah Lainnya' : 0.1,
    'Keluarga Miskin Ekstrem' : 0.1,
    'Kehilangan Mata Pencaharian' : 0.1,
    'Difabel' : 0.1,
    'Penyakit Menahun / Kronis' : 0.1,
    'Rumah Tangga Tunggal / Lansia' : 0.1
}

# Normalisasi semua kolom sesuai jenis kriteria
def normalize_column(series):
    return series / series.max()

for key in weights.keys():
    if pd.api.types.is_numeric_dtype(df[key]):
        df[key + '_N'] = normalize_column(df[key])
    else:
        # Untuk kolom non-numerik, tetapkan skor normalisasi 0 (atau dapat menerapkan pengkodean)
        df[key + '_N'] = 0

# Hitung skor akhir
df['Skor_Akhir'] = 0
for key, weight in weights.items():
    df['Skor_Akhir'] += df[key + '_N'] * weight

# Rekomendasi: urutkan dari skor tertinggi
df_sorted = df.sort_values(by='Skor_Akhir', ascending=False)

# Tampilkan hasil
print("=== Rekomendasi Penerima Bantuan ===")
print(df_sorted[['Nama', 'Skor_Akhir']])
