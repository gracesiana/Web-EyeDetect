# 📦 Daftar Dependencies EyeDetect

## ✅ SUDAH TERINSTALL (di Virtual Environment)

Semua package berikut sudah terinstall di `.venv`:

### 🔧 **Framework Utama**
- ✅ **Django 6.0.7** - Web framework Python
- ✅ **whitenoise 6.12.0** - Static file serving
- ✅ **gunicorn 23.0.0** - Production WSGI server

### 🤖 **AI & Machine Learning**
- ✅ **tensorflow 2.21.0** - Deep learning framework
- ✅ **keras 3.15.0** - High-level neural networks API
- ✅ **numpy 2.5.1** - Numerical computing
- ✅ **opencv-python-headless 5.0.0.93** - Image processing

### 🖼️ **Image Processing**
- ✅ **Pillow 11.2.1** - Python Imaging Library

### 💾 **Database**
- ✅ **psycopg[binary] 3.2.1** - PostgreSQL adapter
- ✅ **sqlparse 0.5.5** - SQL parser

### ☁️ **Cloud Storage (Optional)**
- ✅ **cloudinary 1.41.0** - Cloud image storage
- ✅ **django-cloudinary-storage 0.3.0** - Django integration

### 📚 **Support Libraries**
- ✅ absl-py 2.5.0
- ✅ asgiref 3.11.1
- ✅ certifi 2026.6.17
- ✅ charset-normalizer 3.4.9
- ✅ grpcio 1.82.1
- ✅ h5py 3.14.0
- ✅ requests 2.34.2
- ✅ protobuf 7.35.1

---

## 🎯 YANG HARUS ADA DI SISTEM (Pre-requisites)

Sebelum menjalankan aplikasi, pastikan sudah ada:

### 1. **Python 3.11** ✅
   - Cek dengan: `python --version`
   - Download dari: https://www.python.org/downloads/

### 2. **pip** ✅
   - Sudah include dengan Python
   - Cek dengan: `pip --version`

### 3. **PowerShell** ✅
   - Sudah ada di Windows

---

## 📥 CARA INSTALL (Jika Belum)

Jika virtual environment belum ada atau perlu install ulang:

### **Otomatis (Recommended):**
```powershell
.\setup.ps1
```

### **Manual:**
```powershell
# 1. Buat virtual environment
cd d:\web-eyedetect\Web-EyeDetect\backend
python -m venv .venv

# 2. Aktifkan venv
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install semua dependencies
pip install -r requirements.txt
```

---

## 📊 UKURAN FILE

Estimasi ukuran download dependencies:
- **TensorFlow**: ~350 MB
- **OpenCV**: ~50 MB
- **Django + lainnya**: ~50 MB
- **TOTAL**: ~450-500 MB

Model AI (`eye_disease_model.h5`): ~9 MB

---

## 🔍 CEK STATUS INSTALL

Untuk mengecek apakah semua sudah terinstall:

```powershell
cd d:\web-eyedetect\Web-EyeDetect\backend
.\.venv\Scripts\Activate.ps1
pip list
```

Atau cek package tertentu:
```powershell
pip show django
pip show tensorflow
pip show opencv-python-headless
```

---

## 🚫 TIDAK PERLU INSTALL GLOBAL

Semua dependencies sudah terinstall di **virtual environment** (`.venv`), jadi:
- ❌ TIDAK perlu install Python packages secara global
- ❌ TIDAK perlu install Node.js/npm
- ❌ TIDAK perlu install database server (pakai SQLite)
- ❌ TIDAK perlu install web server (pakai Django dev server)

---

## ⚠️ TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'django'"
➡️ Pastikan virtual environment aktif:
```powershell
.\.venv\Scripts\Activate.ps1
```

### "No module named 'tensorflow'"
➡️ Install ulang dependencies:
```powershell
pip install -r requirements.txt
```

### "Virtual environment not found"
➡️ Jalankan setup dulu:
```powershell
.\setup.ps1
```

---

## 📝 CATATAN

✅ **Status Saat Ini:**
- Virtual environment: **SUDAH ADA** (`.venv`)
- Dependencies: **SUDAH TERINSTALL** (45 packages)
- Server: **SUDAH RUNNING** di http://localhost:8000

🎉 **Aplikasi siap digunakan!** Tidak perlu install apa-apa lagi.

---

**Last Updated:** July 10, 2026
