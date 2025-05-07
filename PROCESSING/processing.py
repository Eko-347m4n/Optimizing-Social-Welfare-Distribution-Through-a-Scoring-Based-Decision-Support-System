import pandas as pd
import numpy as np

# Load data warga
df = pd.read_excel('../DATASET/dataset.xlsx')

# Inisialisasi nilai awal: 10 jika DTKS = 'V' atau '-', selain itu NaN
df['Total_Nilai'] = np.where(df['DTKS'] == 'V', 10, np.nan)
# df['Total_Nilai'] = np.where(df['DTKS'].isin(['V', '-']), 10, np.nan)

# Kolom yang mengurangi skor
pengurang = ['PKH', 'Kartu Pra Kerja', 'BST', 'Bansos Pemerintah Lainnya']

# Kolom Pekerjaan mengurangi skor
pekerjaan_pengurang = ['POLRI', 'PNS', 'TNI']

# Kolom yang menambah skor
penambah = [
    'Keluarga Miskin Ekstrem',
    'Kehilangan Mata Pencaharian',
    'Tidak Berkerja',
    'Difabel',
    'Penyakit Menahun / Kronis',
    'Rumah Tangga Tunggal / Lansia'
]

# Proses penambahan skor
for col in penambah:
    df.loc[df['Total_Nilai'].notna(), 'Total_Nilai'] += (df[col] == 'V').astype(int)
    
# Proses pengurangan skor
for col in pengurang:
    df.loc[df['Total_Nilai'].notna(), 'Total_Nilai'] -= (df[col] == 'V').astype(int)

# Kurangi 10 jika pekerjaan termasuk dalam daftar pekerjaan_pengurang
df.loc[df['Total_Nilai'].notna() & df['Pekerjaan'].isin(pekerjaan_pengurang), 'Total_Nilai'] -= 10

# Tampilkan nama yang memperoleh nilai >= 10 dan jumlahnya
df_filtered = df.loc[df['Total_Nilai'] >= 10, ['Nama', 'Total_Nilai']]
print("\n=== Nama dengan Total Nilai >= 10 ===")
print(df_filtered)
print(f"Jumlah baris: {len(df_filtered)}")
