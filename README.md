# 🎯 Sistem Pendukung Keputusan (SPK) Bantuan Sosial

Proyek ini merupakan implementasi Sistem Pendukung Keputusan (SPK) berbasis klasifikasi dan perangkingan penerima bantuan sosial. SPK ini menggabungkan algoritma **ID3 (Decision Tree), K-NN (K-Nearest Neighbors)** dan **Hybrid SAW (Simple Additive Weighting)** untuk menentukan dan memprioritaskan siapa saja yang layak menerima bantuan berdasarkan sejumlah indikator sosial.

---

## 📦 Deskripsi Setiap Komponen

### 📌 `DATASET/`
Folder ini berisi dataset utama (`dataset.xlsx`) yang telah disiapkan dengan skenario realistis berdasarkan data nama orang Indonesia. Dataset ini **dirandomisasi** menggunakan skrip Python untuk menghasilkan data sosial-ekonomi yang sesuai untuk pengolahan SPK.

---

### 📌 `PROCESSING/`

- `processing.py`  
  Menghitung skor sosial (`Total_Nilai`) berdasarkan status warga seperti DTKS, pekerjaan, difabel, bantuan pemerintah, dll.

- `ID3.py`  
  Implementasi **algoritma ID3** untuk klasifikasi kelayakan bantuan dan **Hybrid SAW** untuk perangkingan. Menghasilkan output evaluasi, struktur pohon, dan hasil ranking.

- `KNN.py` 
   Untuk pengujian alternatif algoritma klasifikasi menggunakan K-Nearest Neighbors.

---

## ⚙️ Cara Menjalankan

Pastikan Anda memiliki:
- Python 3.8+
- Library: `pandas`, `numpy`, `sklearn`, `matplotlib`, `openpyxl`

Instalasi dependensi:

bash
`pip install pandas numpy scikit-learn matplotlib openpyxl`

Lalu jalankan:
`cd PROCESSING`
`python3 ID3.py` sesuaikan dengan algoritma apa yang ingin digunakan

---

## 📌 Catatan
Proyek ini dapat digunakan untuk skenario nyata, analisis sosial.
Namun, pastikan Anda:
Menyesuaikan kategori indikator sosial sesuai konteks lokal.
Memperbarui dataset (dataset.xlsx) agar valid dan relevan.
