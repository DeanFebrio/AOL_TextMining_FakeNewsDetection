# 🚀 Panduan Setup Environment Proyek

Dokumentasi ini menjelaskan langkah-langkah untuk mengunduh proyek, membuat *virtual environment* Python, mengaktifkannya, serta menginstal seluruh dependensi yang dibutuhkan agar proyek dapat dijalankan dengan baik.

---

## 📋 Prasyarat

Sebelum memulai, pastikan hal-hal berikut sudah tersedia pada komputer Anda:

* Python **3.8 atau lebih baru** (disarankan Python 3.10+)
* Git telah terinstal
* Koneksi internet untuk mengunduh dependensi
* Terminal atau PowerShell

Untuk memverifikasi instalasi Python dan Git, jalankan:

```bash
python --version
git --version
```

---

## 📥 1. Clone Repository

Unduh proyek dari GitHub dan masuk ke direktori proyek:

```bash
git clone https://github.com/DeanFebrio/AOL_TextMining_FakeNewsDetection.git
cd AOL_TextMining_FakeNewsDetection
```

---

## 🐍 2. Membuat Virtual Environment

Buat *virtual environment* dengan nama `.venv`:

```bash
python -m venv .venv
```

Perintah ini akan membuat folder `.venv` yang berisi lingkungan Python terisolasi untuk proyek ini.

---

## ⚡ 3. Mengaktifkan Virtual Environment

Aktifkan *virtual environment* sesuai terminal yang digunakan.

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate
```

### Windows (Command Prompt)

```cmd
.venv\Scripts\activate.bat
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Jika berhasil, Anda akan melihat awalan seperti berikut pada terminal:

```text
(.venv) C:\Users\Username\AOL_TextMining_FakeNewsDetection>
```

---

## 📦 4. Menginstal Dependensi

Pastikan virtual environment sudah aktif, kemudian jalankan:

```bash
python -m pip install -r requirements.txt
```

Proses ini akan menginstal seluruh library yang diperlukan oleh proyek.

---

## ✅ 5. Verifikasi Instalasi

Untuk memastikan seluruh paket berhasil terinstal, jalankan:

```bash
pip list
```

Pastikan paket-paket yang tercantum pada `requirements.txt` muncul pada daftar hasil instalasi.

Anda juga dapat memeriksa apakah terdapat dependensi yang belum terinstal dengan:

```bash
pip check
```

---

## ▶️ Menjalankan Proyek

Setelah seluruh dependensi berhasil terinstal, proyek siap dijalankan.

Gunakan perintah yang sesuai dengan dokumentasi atau file utama proyek, misalnya:

```bash
python main.py
```

> Sesuaikan nama file dengan entry point utama proyek Anda.

---

## 🔄 Mengaktifkan Kembali Environment

Jika Anda menutup terminal dan ingin melanjutkan pekerjaan di lain waktu, cukup masuk ke folder proyek lalu aktifkan kembali virtual environment:

```powershell
.venv\Scripts\Activate
```

Tidak perlu membuat ulang virtual environment maupun menginstal ulang dependensi.

---

## 🛑 Menonaktifkan Virtual Environment

Untuk keluar dari virtual environment, jalankan:

```bash
deactivate
```

Setelah dinonaktifkan, awalan `(.venv)` pada terminal akan hilang.

---

## ⚠️ Troubleshooting

### Execution Policy Error (PowerShell)

Jika muncul pesan seperti:

```text
running scripts is disabled on this system
```

Jalankan PowerShell sebagai Administrator, kemudian:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Lalu coba aktifkan kembali virtual environment.

---

### Python Tidak Ditemukan

Jika muncul pesan:

```text
'python' is not recognized as an internal or external command
```

Pastikan Python sudah terinstal dan telah ditambahkan ke PATH sistem.

---

### Gagal Menginstal Dependensi

Perbarui pip terlebih dahulu:

```bash
python -m pip install --upgrade pip
```

Kemudian ulangi proses instalasi:

```bash
python -m pip install -r requirements.txt
```

---
