import pandas as pd
import numpy as np

# Load data nama dari CSV
names_df = pd.read_csv("indonesian-names.csv")
names_df = names_df[['name']]  # Select only the 'name' column
names_df.columns = ['Nama']  # Rename the column to 'Nama'

n = len(names_df)

# 1. Pekerjaan (25% masing-masing)
jobs = ['PNS', 'TNI', 'POLRI', 'Buruh']
pelajar_count = int(n * 0.10)
other_count = n - pelajar_count
other_jobs = np.tile(jobs, other_count // len(jobs))
if len(other_jobs) < other_count:
    other_jobs = np.append(other_jobs, np.random.choice(jobs, size=other_count - len(other_jobs)))
pekerjaan = np.append(other_jobs, ['Pelajar'] * pelajar_count)
np.random.shuffle(pekerjaan)

# 2. DTKS (default)
dtks = np.random.choice(['V', '-'], size=n, p=[0.25, 0.75])

# 3. Menerima JPS
jps_programs = ['PKH', 'Kartu Pra Kerja', 'BST', 'Bansos Pemerintah Lainnya']
jps_menerima = pd.DataFrame('-', index=range(n), columns=jps_programs)
idx_jps = np.random.choice(n, int(n * 0.75), replace=False)

for i in idx_jps:
    selected = np.random.choice(jps_programs, np.random.randint(1, 3), replace=False)
    for program in selected:
        jps_menerima.loc[i, program] = 'V'

# 4. Belum Menerima JPS
belum_jps = ['Keluarga Miskin Ekstrem', 'Kehilangan Mata Pencaharian', 'Tidak Berkerja', 'Difabel',
             'Penyakit Menahun / Kronis', 'Rumah Tangga Tunggal / Lansia']
belum_menerima = pd.DataFrame('-', index=range(n), columns=belum_jps)
idx_belum = list(set(range(n)) - set(idx_jps))

for i in idx_belum:
    selected = np.random.choice(belum_jps, np.random.randint(1, 3), replace=False)
    for alasan in selected:
        belum_menerima.loc[i, alasan] = 'V'

# 5. Perbarui semua jika pekerjaan == PNS, TNI, POLRI
for i in range(n):
    if pekerjaan[i] in ['PNS', 'TNI', 'POLRI']:
        dtks[i] = '-'
        jps_menerima.loc[i] = '-'
        belum_menerima.loc[i] = '-'

# 6. Perbarui semua jika menerima PKH == Terdata DTKS
for i in range(n):
    if jps_menerima.loc[i, 'PKH'] == 'V':
        dtks[i] = 'V'

# 7. Gabungkan semua
final_df = pd.concat([
    names_df,
    pd.Series(pekerjaan, name='Pekerjaan'),
    pd.Series(dtks, name='DTKS'),
    jps_menerima,
    belum_menerima,
], axis=1)

# Simpan hasil
final_df.to_excel("dataset.xlsx", index=False)