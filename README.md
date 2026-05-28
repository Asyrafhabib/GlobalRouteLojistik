# Global Route Lojistik

Aplikasi desktop manajemen logistik modern untuk operasional kargo, pelanggan, cabang, dan riwayat pengiriman. Dibangun dengan PyQt6 untuk antarmuka pengguna yang responsif dan MySQL untuk penyimpanan data.

## Fitur Utama

- Manajemen pelanggan: tambah, ubah, hapus, dan lihat daftar pelanggan.
- Pengelolaan pengiriman kargo: pembuatan pengiriman, hitung biaya otomatis, update status, dan tampilan riwayat.
- Modul cabang: kelola data kantor cabang dan lokasi.
- Layanan riwayat gerakan kargo: catat dan lihat pergerakan pengiriman.
- Sidebar modern dengan animasi dan ikon SVG kustom.
- Tema gelap profesional dengan styling antarmuka yang konsisten.

## Arsitektur Proyek

- `main.py`: Titik masuk aplikasi.
- `UI/`: Semua komponen tampilan.
  - `main_window.py`: Jendela utama dan navigasi aplikasi.
  - `pages.py`: Halaman fitur untuk `Müşteri`, `Gönderi`, `Şube`, dan `Hareket`.
  - `theme.py`: Tema dan stylesheet untuk seluruh aplikasi.
  - `icons.py`: Penyimpanan ikon SVG dan helper untuk memuat ikon.
- `BLL/`: Logika bisnis aplikasi.
  - `kargo_logic.py`: Validasi data, perhitungan biaya otomatis, dan panggilan ke lapisan DAL.
- `DAL/`: Akses data ke database MySQL.
  - `kargo_dal.py`: Fungsi CRUD yang memanggil stored procedure MySQL.

## Teknologi

- Python 3.14+
- PyQt6
- MySQL
- geopy (untuk kalkulasi jarak menggunakan Nominatim/OpenStreetMap)
- SVG untuk ikon dan branding

## Prasyarat

Pastikan sudah menginstal:

- Python 3.14 atau lebih tinggi
- PyQt6
- mysql-connector-python
- geopy
- MySQL server dengan database `globalroute_db` dan stored procedure yang diperlukan

## Instalasi & Jalankan

1. Kloning atau salin repositori ke mesin Anda.
2. Masuk ke folder proyek:
   ```bash
   cd c:\Users\asyra\Documents\Mine\Projeler\GlobalRouteLojistik
   ```
3. Install dependensi Python:
   ```bash
   pip install PyQt6 mysql-connector-python geopy
   ```
4. Jalankan aplikasi:
   ```bash
   python main.py
   ```

## Konfigurasi Database

File `DAL/kargo_dal.py` menggunakan koneksi MySQL berikut:

- host: `localhost`
- user: `root`
- password: `asyraf12345`
- database: `globalroute_db`

Sesuaikan kredensial ini jika diperlukan.

## Catatan Penting

- Modul `kargo_logic.py` menggunakan `geopy.Nominatim` untuk mendapatkan koordinat lokasi dari nama kota, lalu menghitung jarak menggunakan `geodesic`.
- Jika API geocoding tidak tersedia, sistem akan menggunakan fallback perhitungan tarif berbasis berat.

## Ide Pengembangan

- Tambahkan validasi input dan notifikasi lebih kaya.
- Koneksikan dengan cadangan offline ketika MySQL tidak tersedia.
- Perluas laporan analitik pengiriman dan kinerja cabang.

## Lisensi

Gunakan sesuai kebutuhan Anda. Silakan tambahkan lisensi pilihan jika ingin membagikan proyek ini secara publik.
