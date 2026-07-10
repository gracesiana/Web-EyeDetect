# 🚀 Installation Guide - EyeDetect

Panduan lengkap untuk kontributor yang ingin menjalankan project ini setelah clone dari GitHub.

---

## 📋 Prerequisites (Yang Harus Diinstall Dulu)

Sebelum mulai, pastikan sistem Anda sudah punya:

### 1. **Python 3.10, 3.11, atau 3.12** ✅

**Cek apakah sudah ada:**
```powershell
python --version
```
atau
```powershell
py --version
```

**Jika belum ada, download dari:**
- 🔗 https://www.python.org/downloads/

**Catatan Instalasi Python:**
- ✅ Centang "Add Python to PATH" saat install
- ✅ Pilih "Install for all users" (recommended)
- ✅ Setelah install, restart terminal/PowerShell

---

### 2. **pip** (Python Package Manager) ✅

pip biasanya sudah include dengan Python. Cek dengan:
```powershell
pip --version
```

Jika belum ada, install dengan:
```powershell
python -m ensurepip --upgrade
```

---

### 3. **Git** (Optional, untuk clone repo) ✅

**Cek:**
```powershell
git --version
```

**Download:**
- 🔗 https://git-scm.com/downloads

---

## 📥 Langkah 1: Clone Repository

```powershell
# Clone dari GitHub
git clone https://github.com/gracesiana/Web-EyeDetect.git

# Masuk ke folder project
cd Web-EyeDetect
```

Atau download ZIP dari GitHub dan extract.

---

## ⚙️ Langkah 2: Setup Project

Ada 2 cara: **Otomatis** (Recommended) atau **Manual**

---

### 🎯 **CARA 1: Setup Otomatis (Recommended)**

Cukup jalankan script setup yang sudah disediakan:

```powershell
.\setup.ps1
```

Script ini akan otomatis:
- ✅ Membuat virtual environment (`.venv`)
- ✅ Install semua dependencies dari `requirements.txt`
- ✅ Setup database (SQLite)
- ✅ Membuat admin user default

⏱️ **Waktu:** ~5-10 menit (tergantung internet)

**Setelah selesai, lanjut ke Langkah 3!**

---

### 🔧 **CARA 2: Setup Manual**

Jika setup otomatis gagal atau ingin install manual:

#### **2.1. Buat Virtual Environment**
```powershell
cd backend
python -m venv .venv
```

#### **2.2. Aktifkan Virtual Environment**
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Git Bash
source .venv/Scripts/activate
```

**Tanda venv aktif:** Ada `(.venv)` di awal baris terminal

#### **2.3. Upgrade pip**
```powershell
python -m pip install --upgrade pip
```

#### **2.4. Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Dependencies yang akan diinstall:**
- Django 6.0.7 (~10 MB)
- TensorFlow 2.18.0 (~350 MB) ⚠️ File besar!
- OpenCV Python Headless (~50 MB)
- Pillow 11.2.1
- NumPy 1.26.4
- WhiteNoise 6.12.0
- PostgreSQL adapter (psycopg) 3.2.1
- Gunicorn 23.0.0
- Cloudinary 1.41.0 (optional)

💡 **Total download:** ~450-500 MB

⏱️ **Waktu install:** 5-15 menit tergantung internet

#### **2.5. Setup Database**
```powershell
python manage.py migrate
```

#### **2.6. Buat Admin User**
```powershell
python manage.py ensure_default_admin
```

Atau buat manual:
```powershell
python manage.py createsuperuser
```

---

## 🚀 Langkah 3: Jalankan Server

### **Cara Mudah (Otomatis):**
```powershell
# Dari root folder
.\run.ps1
```

### **Cara Manual:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Server akan berjalan di:
- 🌐 http://localhost:8000/
- 🌐 http://127.0.0.1:8000/

---

## 🔐 Login Credentials

### **Admin:**
- URL: http://localhost:8000/login/admin/
- Username: `admin`
- Email: `admin@retinadetect.local`
- Password: `admin123`

### **User Biasa:**
- Daftar di: http://localhost:8000/daftar/

---

## 🛑 Stop Server

Tekan **CTRL + C** di terminal

---

## 📂 Struktur Project Setelah Setup

```
Web-EyeDetect/
├── backend/
│   ├── .venv/                    👈 Virtual environment (muncul setelah setup)
│   ├── ai_model/
│   │   ├── eye_disease_model.h5  👈 Model AI (9 MB)
│   │   ├── predict.py
│   │   └── gradcam.py
│   ├── EyeDetect/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── appdeteksi/
│   ├── media/                    👈 Uploaded images
│   ├── staticfiles/              👈 Static files (muncul setelah collectstatic)
│   ├── db.sqlite3                👈 Database (muncul setelah migrate)
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── user/                     👈 User templates
│   ├── admin/                    👈 Admin templates
│   └── component/                👈 CSS, JS, images
├── setup.ps1                     👈 Setup script
├── run.ps1                       👈 Run server script
└── README.md
```

---

## ⚠️ Troubleshooting

### **1. Error: "cannot be loaded because running scripts is disabled"**

Jalankan PowerShell sebagai **Administrator**, lalu:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Lalu coba lagi.

---

### **2. Error: "Python is not recognized"**

Python belum ada di PATH. Solusi:
1. Reinstall Python dengan centang "Add Python to PATH"
2. Atau tambahkan manual ke PATH
3. Restart terminal setelah install

---

### **3. Error: "ModuleNotFoundError: No module named 'django'"**

Virtual environment belum aktif. Aktifkan dulu:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
```

---

### **4. Error saat install TensorFlow**

TensorFlow butuh file besar (~350 MB). Solusi:
- Pastikan internet stabil
- Coba install ulang:
  ```powershell
  pip install tensorflow==2.18.0 --no-cache-dir
  ```

---

### **5. Error: "Port 8000 already in use"**

Ada aplikasi lain yang pakai port 8000. Solusi:
```powershell
# Jalankan di port lain
python manage.py runserver 8080
```

Atau stop aplikasi yang pakai port 8000.

---

### **6. Model file not found**

Pastikan file `ai_model/eye_disease_model.h5` ada. File ini harus:
- ✅ Ada di folder `backend/ai_model/`
- ✅ Ukuran ~9 MB
- ✅ Tidak corrupt

---

## 🔄 Update Dependencies

Jika ada update di `requirements.txt`:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade
```

---

## 🧹 Reset/Clean Install

Jika ingin install ulang dari awal:

```powershell
# Hapus virtual environment
cd backend
Remove-Item -Recurse -Force .venv

# Hapus database
Remove-Item db.sqlite3

# Jalankan setup lagi
cd ..
.\setup.ps1
```

---

## 📊 Checklist Instalasi

Sebelum mulai development, pastikan:

- [ ] Python 3.10+ terinstall
- [ ] pip terinstall
- [ ] Repository sudah di-clone
- [ ] Virtual environment sudah dibuat (`.venv`)
- [ ] Dependencies sudah terinstall (`pip list` shows Django, TensorFlow, dll)
- [ ] Database sudah di-migrate (`db.sqlite3` ada)
- [ ] Admin user sudah dibuat
- [ ] Server bisa running (`python manage.py runserver`)
- [ ] Bisa akses http://localhost:8000/

---

## 🤝 Untuk Kontributor

Setelah setup selesai:

1. **Branch untuk development:**
   ```bash
   git checkout -b feature/nama-fitur
   ```

2. **Activate venv sebelum coding:**
   ```powershell
   cd backend
   .\.venv\Scripts\Activate.ps1
   ```

3. **Testing:**
   ```powershell
   python manage.py test
   ```

4. **Commit & Push:**
   ```bash
   git add .
   git commit -m "Add: deskripsi perubahan"
   git push origin feature/nama-fitur
   ```

---

## 📞 Butuh Bantuan?

- 📖 Baca: [README.md](./README.md)
- 🐛 Issue: [GitHub Issues](https://github.com/gracesiana/Web-EyeDetect/issues)
- 📧 Email: (your-email@example.com)

---

**Happy Coding! 🎉**

Made with ❤️ for better eye health screening
