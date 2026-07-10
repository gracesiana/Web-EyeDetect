# ⚡ Quick Start Guide - EyeDetect

## 🚀 Setup Pertama Kali (One-Time Setup)

### Otomatis (Recommended):
```powershell
# Klik kanan setup.ps1 → Run with PowerShell
# atau jalankan di PowerShell:
.\setup.ps1
```

### Manual:
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install Django tensorflow numpy Pillow opencv-python-headless cloudinary django-cloudinary-storage whitenoise
python manage.py migrate
python manage.py ensure_default_admin
python manage.py runserver
```

---

## 🏃 Run Server (Setelah Setup)

### Otomatis:
```powershell
# Klik kanan run.ps1 → Run with PowerShell
# atau:
.\run.ps1
```

### Manual:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## 🌐 Access

- **Web**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **Username**: `admin`
- **Password**: `admin123`

---

## 🛑 Stop Server

Tekan **CTRL + C** di terminal

---

## 📚 Dokumentasi Lengkap

Lihat [CARA_RUN_PROJECT.md](./CARA_RUN_PROJECT.md) untuk dokumentasi lengkap.
