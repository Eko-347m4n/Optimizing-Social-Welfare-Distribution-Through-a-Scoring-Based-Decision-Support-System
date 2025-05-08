import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample

# ===============================
# 1. Load dan Proses Data
# ===============================
df = pd.read_excel('../DATASET/dataset.xlsx')

# Inisialisasi skor awal berdasarkan DTKS
df['Total_Nilai'] = np.where(df['DTKS'] == 'V', 10, np.nan)

# Kriteria penambah dan pengurang skor
penambah = [
    'Keluarga Miskin Ekstrem', 'Kehilangan Mata Pencaharian', 'Tidak Berkerja',
    'Difabel', 'Penyakit Menahun / Kronis', 'Rumah Tangga Tunggal / Lansia'
]

pengurang = [
    'PKH', 'Kartu Pra Kerja', 'BST', 'Bansos Pemerintah Lainnya'
]

# Tambahkan poin dari kriteria penambah
for col in penambah:
    df.loc[df['Total_Nilai'].notna(), 'Total_Nilai'] += (df[col] == 'V').astype(int)

# Kurangi poin dari kriteria pengurang
for col in pengurang:
    df.loc[df['Total_Nilai'].notna(), 'Total_Nilai'] -= (df[col] == 'V').astype(int)

# Tentukan kelayakan
df['Layak'] = df['Total_Nilai'].apply(lambda x: 'Ya' if x >= 10 else 'Tidak')

# ===============================
# 2. Klasifikasi ID3 + Oversampling
# ===============================
features = penambah + pengurang
X = df[features].replace({'V': 1, '-': 0, np.nan: 0}).infer_objects(copy=False)
y = df['Layak']

# Oversampling data minoritas
df_model = pd.concat([X, y], axis=1)
df_majority = df_model[df_model['Layak'] == 'Tidak']
df_minority = df_model[df_model['Layak'] == 'Ya']

df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

df_balanced = pd.concat([df_majority, df_minority_upsampled])
X_balanced = df_balanced[features]
y_balanced = df_balanced['Layak']

# Split data latih dan uji
X_train, X_test, y_train, y_test = train_test_split(
    X_balanced, y_balanced, test_size=0.2, random_state=42
)

# Latih model ID3 (Decision Tree)
clf = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Evaluasi
print("=== EVALUASI MODEL ID3 ===")
print("Akurasi:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Tampilkan struktur pohon keputusan
print("\n=== STRUKTUR POHON KEPUTUSAN ===")
print(export_text(clf, feature_names=features))

# ===============================
# 3. Hybrid SAW Ranking
# ===============================
df_saw = df[df['Total_Nilai'].notna()].copy()
df_saw['Skor_Ternormalisasi'] = df_saw['Total_Nilai'] / df_saw['Total_Nilai'].max()
df_saw['Skor_Akhir'] = df_saw['Skor_Ternormalisasi'] * 1  # Bobot 1

df_saw = df_saw.sort_values(by='Skor_Akhir', ascending=False)

df_saw_passing = df_saw[df_saw['Total_Nilai'] >= 10]

print("\n=== RANKING DATA DENGAN PASSING GRADE 10 (HYBRID SAW) ===")
print(df_saw_passing[['Nama', 'Total_Nilai', 'Skor_Akhir']])

# ===============================
# 4. Visualisasi Pohon Keputusan
# ===============================
plt.figure(figsize=(20, 10))
plot_tree(clf, feature_names=features, class_names=['Tidak', 'Ya'], filled=True)
plt.title("Pohon Keputusan - ID3")
plt.show()
