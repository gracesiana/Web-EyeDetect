# 📁 Guide File-File dalam Project

## 📄 File Setup & Running

### **setup.ps1** 🔧
Script PowerShell untuk setup project otomatis (first-time setup).

**Cara Pakai:**
- Klik kanan → "Run with PowerShell"
- Atau di PowerShell: `.\setup.ps1`

**Fungsi:**
- Buat virtual environment
- Install semua dependencies
- Setup database
- Buat admin user

---

### **run.ps1** ▶️
Script PowerShell untuk run development server.

**Cara Pakai:**
- Klik kanan → "Run with PowerShell"
- Atau di PowerShell: `.\run.ps1`

**Fungsi:**
- Aktifkan virtual environment
- Check migrations
- Start Django server

---

### **QUICKSTART.md** ⚡
Quick reference untuk setup dan run project (versi singkat).

---

### **CARA_RUN_PROJECT.md** 📚
Dokumentasi lengkap step-by-step cara run project.

Isi:
- Prerequisites
- Setup lengkap
- Troubleshooting
- Default credentials
- URL access

---

### **README.md** 📖
Dokumentasi utama project (overview, features, tech stack).

---

## 📁 Folder Structure

### **backend/** 
Folder utama Django backend.

**File Penting:**
- `manage.py` - Django management script
- `db.sqlite3` - Database (dibuat otomatis)
- `.venv/` - Virtual environment (dibuat saat setup)

**Sub-folders:**
- `ai_model/` - AI model & prediction logic
- `appdeteksi/` - Django app utama (models, views)
- `EyeDetect/` - Project settings & configuration
- `media/` - Upload images (dibuat otomatis)

---

### **frontend/**
Folder untuk templates HTML & static files.

**Sub-folders:**
- `user/` - Template untuk user interface
- `admin/` - Template untuk admin panel
- `component/` - Static assets (images, CSS, JS)

---

### **ai_model/**
Folder berisi AI model & prediction.

**File:**
- `eye_disease_model.h5` - Trained TensorFlow model
- `predict.py` - Prediction logic
- `gradcam.py` - Grad-CAM visualization
- `train.py` - Model training script

---

## 📝 File Konfigurasi

### **requirements.txt**
Daftar Python packages yang dibutuhkan.

**Isi utama:**
- Django 6.0.7
- TensorFlow 2.17.0
- OpenCV
- Pillow (image processing)
- Cloudinary (cloud storage)

---

### **.env.example**
Template environment variables untuk production.

**Untuk local development tidak wajib**, tapi bisa di-copy ke `.env` jika mau kustomisasi.

---

### **.gitignore**
File untuk ignore files dari Git (venv, cache, database, media).

---

## 🚀 Workflow Run Project

### First Time:
```
1. setup.ps1           → Setup semua
2. run.ps1             → Run server
3. Browser → localhost:8000
```

### Next Times:
```
1. run.ps1             → Run server
2. Browser → localhost:8000
```

### Manual (tanpa script):
```
1. cd backend
2. .\.venv\Scripts\Activate.ps1
3. python manage.py runserver
4. Browser → localhost:8000
```

---

## 🎯 File Mana yang Harus Dibaca?

### Untuk Setup:
1. **QUICKSTART.md** - Baca dulu ini (paling singkat)
2. **CARA_RUN_PROJECT.md** - Kalau ada masalah, baca ini
3. **README.md** - Untuk overview project

### Untuk Development:
- `backend/EyeDetect/settings.py` - Django settings
- `backend/EyeDetect/views.py` - Main views
- `backend/appdeteksi/models.py` - Database models
- `backend/ai_model/predict.py` - AI prediction logic

---

## 🔐 File Credentials

**Default Admin:**
- Username: `admin`
- Password: `admin123`

Dibuat otomatis oleh:
```
python manage.py ensure_default_admin
```

---

## 📞 Need Help?

Baca file ini secara berurutan:
1. **QUICKSTART.md** ⚡ (5 menit)
2. **CARA_RUN_PROJECT.md** 📚 (lengkap + troubleshooting)
3. **README.md** 📖 (overview project)

Atau langsung run:
```powershell
.\setup.ps1   # Setup
.\run.ps1     # Run
```

---

**Happy Coding! 🚀**
