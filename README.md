# Proyek Sistem Pendukung Keputusan (SPK) - Kelayakan Bantuan Sosial

Proyek ini bertujuan untuk membangun Sistem Pendukung Keputusan (SPK) guna menentukan kelayakan calon penerima bantuan sosial. SPK ini menggunakan beberapa kriteria untuk menghitung skor kelayakan dan kemudian melakukan klasifikasi serta perankingan.

## Daftar Isi

- [Deskripsi Proyek](#deskripsi-proyek)
- [Struktur Proyek](#struktur-proyek)
- [Dataset](#dataset)
- [Metodologi](#metodologi)
  - [1. Pemuatan dan Pra-pemrosesan Data](#1-pemuatan-dan-pra-pemrosesan-data)
  - [2. Klasifikasi](#2-klasifikasi)
    - [Algoritma ID3 (Decision Tree)](#algoritma-id3-decision-tree)
    - [Algoritma KNN (K-Nearest Neighbors)](#algoritma-knn-k-nearest-neighbors)
    - [Oversampling](#oversampling)
  - [3. Perankingan (Hybrid SAW)](#3-perankingan-hybrid-saw)
- [Instalasi](#instalasi)
- [Cara Menjalankan](#cara-menjalankan)
- [Output](#output)

## Deskripsi Proyek

Sistem ini dirancang untuk membantu dalam proses pengambilan keputusan terkait penyaluran bantuan sosial. Proses utama meliputi:

1. **Penghitungan Skor Awal**: Berdasarkan status DTKS (Data Terpadu Kesejahteraan Sosial).
2. **Penyesuaian Skor**: Menambah atau mengurangi skor berdasarkan kriteria-kriteria tertentu seperti kondisi ekonomi, status pekerjaan, kepemilikan aset, dan penerimaan bantuan lain.
3. **Penentuan Kelayakan Awal**: Berdasarkan skor total yang diperoleh.
4. **Klasifikasi**: Menggunakan model Machine Learning (ID3 dan KNN) untuk memprediksi kelayakan berdasarkan fitur-fitur yang ada.
5. **Perankingan**: Menggunakan metode Simple Additive Weighting (SAW) untuk merangking calon penerima yang dianggap layak.

## Struktur Proyek

```
PROYEK_SPK/
├── DATASET/
│   └── dataset.xlsx
├── PROCESSING/
│   ├── ID3.py
│   ├── KNN.py
│   └── processing.py  // Skrip pemrosesan data tambahan/awal
└── README.md
```

## Dataset

Dataset yang digunakan adalah `dataset.xlsx` yang berisi informasi mengenai calon penerima bantuan. Kolom-kolom penting meliputi:

- `DTKS`: Status dalam Data Terpadu Kesejahteraan Sosial.
- Kriteria Penambah Skor: `Keluarga Miskin Ekstrem`, `Kehilangan Mata Pencaharian`, `Tidak Berkerja`, `Difabel`, `Penyakit Menahun / Kronis`, `Rumah Tangga Tunggal / Lansia`.
- Kriteria Pengurang Skor: `PKH`, `Kartu Pra Kerja`, `BST`, `Bansos Pemerintah Lainnya`.
- `Pekerjaan`: Jenis pekerjaan (digunakan dalam `processing.py` untuk pengurangan skor tambahan jika pekerjaan termasuk POLRI, PNS, TNI).

## Metodologi

### 1. Pemuatan dan Pra-pemrosesan Data

- Data dimuat dari file `dataset.xlsx`.
- **Inisialisasi Skor**: Skor awal (`Total_Nilai`) adalah 10 jika `DTKS` bernilai 'V', dan `NaN` jika tidak.
- **Penambahan Skor**: Skor ditambah 1 untuk setiap kriteria penambah yang bernilai 'V'.
  - Kriteria: `Keluarga Miskin Ekstrem`, `Kehilangan Mata Pencaharian`, `Tidak Berkerja`, `Difabel`, `Penyakit Menahun / Kronis`, `Rumah Tangga Tunggal / Lansia`.
- **Pengurangan Skor**:
  - Skor dikurangi 1 untuk setiap kriteria pengurang yang bernilai 'V'.
    - Kriteria: `PKH`, `Kartu Pra Kerja`, `BST`, `Bansos Pemerintah Lainnya`.
  - (Dalam `processing.py`) Skor dikurangi 10 jika kolom `Pekerjaan` termasuk dalam kategori `POLRI`, `PNS`, atau `TNI`.
- **Penentuan Kelayakan**: `Layak` bernilai 'Ya' jika `Total_Nilai` >= 10, dan 'Tidak' jika sebaliknya.
- Fitur untuk model klasifikasi (`X`) diambil dari kolom kriteria penambah dan pengurang, dengan nilai 'V' diubah menjadi 1, dan '-' atau `NaN` menjadi 0.
- Target klasifikasi (`y`) adalah kolom `Layak`.

### 2. Klasifikasi

Sebelum melatih model, dilakukan teknik *oversampling* pada kelas minoritas ('Ya') untuk menyeimbangkan dataset.

#### Algoritma ID3 (Decision Tree)

- Menggunakan `DecisionTreeClassifier` dari `sklearn` dengan kriteria `entropy`.
- `max_depth` diatur untuk mengontrol kompleksitas pohon.
- Model dievaluasi menggunakan akurasi dan *classification report*.
- Struktur pohon keputusan divisualisasikan.

#### Algoritma KNN (K-Nearest Neighbors)

- Menggunakan `KNeighborsClassifier` dari `sklearn` dengan `n_neighbors=5` (jumlah tetangga).
- Model dievaluasi menggunakan akurasi dan *classification report*.

#### Oversampling

- Data kelas minoritas (penerima yang 'Layak') di-resample (dengan penggantian) hingga jumlahnya sama dengan data kelas mayoritas (penerima yang 'Tidak Layak'). Ini dilakukan untuk mengatasi ketidakseimbangan kelas.

### 3. Perankingan (Hybrid SAW)

- Metode Simple Additive Weighting (SAW) digunakan untuk merangking data yang memiliki `Total_Nilai` yang valid.
- **Normalisasi Skor**: `Skor_Ternormalisasi` dihitung dengan membagi `Total_Nilai` setiap individu dengan `Total_Nilai` maksimum.
- **Skor Akhir**: Dihitung dengan mengalikan `Skor_Ternormalisasi` dengan bobot (dalam kasus ini, bobot = 1).
- Hasil perankingan diurutkan dari skor tertinggi ke terendah.
- Hanya data dengan `Total_Nilai` >= 10 yang ditampilkan dalam hasil perankingan akhir.

## Instalasi

Pastikan Anda memiliki Python dan pustaka berikut terinstal:

- pandas
- numpy
- scikit-learn
- matplotlib (untuk visualisasi pohon ID3)

Anda dapat menginstalnya menggunakan pip:

```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

## Cara Menjalankan

1. Pastikan file `dataset.xlsx` berada di dalam direktori `DATASET/`.
2. Jalankan skrip Python yang diinginkan dari direktori `PROCESSING/`:

   ```bash
   python ID3.py
   ```

   atau
   ```bash
   python KNN.py
   ```

   Anda juga bisa menjalankan `processing.py` untuk melihat hasil pemrosesan data awal:
   ```bash
   python processing.py
   ```

## Output

- **Evaluasi Model**: Akurasi dan laporan klasifikasi (presisi, recall, f1-score) untuk model ID3 dan KNN.
- **Struktur Pohon Keputusan**: Teks dan visualisasi grafis dari pohon keputusan yang dihasilkan oleh model ID3.
- **Ranking Data**: Daftar nama beserta `Total_Nilai` dan `Skor_Akhir` (hasil SAW) untuk calon penerima yang memenuhi passing grade (Total_Nilai >= 10), diurutkan berdasarkan skor akhir tertinggi.
- **Daftar Nama (dari `processing.py`)**: Daftar nama yang memiliki `Total_Nilai` >= 10 beserta jumlahnya.

---

Semoga dokumentasi ini membantu!
