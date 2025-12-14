# 🔩 Smart Object Counter Pro

**Smart Object Counter Pro** adalah aplikasi Computer Vision berbasis **Streamlit** yang dirancang untuk menghitung jumlah objek kecil (seperti baut, mur, biji-bijian, atau tablet) secara otomatis menggunakan metode *Image Processing* klasik (Non-Machine Learning).

![Tampilan Aplikasi](screenshot.png)
*(Pastikan Anda mengupload screenshot aplikasi dengan nama file screenshot.png agar gambar muncul di sini)*

## 🌟 Fitur Utama

* **Deteksi Otomatis:** Menggunakan alur pemrosesan citra lengkap:
    * *Grayscale* & *Gaussian Blur* (Pengurangan noise).
    * *Thresholding* (Segmentasi biner).
    * *Morphology* (Pembersihan noise & penutupan lubang).
    * *Contour Analysis* (Deteksi tepi objek).
* **Visualisasi Bounding Box:** Menandai setiap objek yang terdeteksi dengan kotak hijau (Rectangle) dan nomor urut.
* **Filter Interaktif:** Slider untuk mengatur tingkat Blur, Threshold, dan Area Minimum (untuk mengabaikan debu/partikel kecil).
* **Antarmuka Cyberpunk:** Desain UI modern dengan animasi CSS, *running text*, dan ikon interaktif.
* **Ekspor Data:** Unduh laporan hasil hitungan ke Excel (.xlsx) atau simpan gambar hasil deteksi.
* **Mode Demo:** Tersedia gambar contoh bawaan untuk pengujian instan tanpa perlu unggah gambar.

## 🛠️ Teknologi yang Digunakan

* **Python 3.x**: Bahasa pemrograman utama.
* **Streamlit**: Framework untuk membuat antarmuka web interaktif.
* **OpenCV**: Library utama untuk pengolahan citra digital.
* **NumPy**: Komputasi numerik array.
* **Pandas**: Manipulasi data untuk tabel dan ekspor Excel.
* **Matplotlib**: Pembuatan grafik visualisasi.

## 🚀 Cara Menjalankan di Komputer Lokal

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer Anda:

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/username-anda/smart-object-counter.git](https://github.com/username-anda/smart-object-counter.git)
    ```

2.  **Masuk ke direktori folder:**
    ```bash
    cd smart-object-counter
    ```

3.  **Install library yang dibutuhkan:**
    Disarankan menggunakan *virtual environment*.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi:**
    ```bash
    streamlit run FixBeneran.py
    ```

## 📂 Struktur File

* `FixBeneran.py`: Kode utama aplikasi (Main Code).
* `requirements.txt`: Daftar dependensi/library Python.
* `README.md`: Dokumentasi proyek ini.

## 🤝 Kontribusi

Proyek ini dibuat untuk tujuan edukasi dan demonstrasi teknik *Computer Vision* dasar. Jika Anda ingin berkontribusi atau memberikan saran, silakan buat *Issue* atau *Pull Request*.

---
**Dibuat dengan ❤️ menggunakan Python & Streamlit**