# ⚡ Quick Start Guide

Panduan singkat untuk kontributor yang baru clone repo.

---

## 📋 Yang Harus Diinstall di Sistem

Sebelum mulai, pastikan sudah punya:

1. **Python 3.10/3.11/3.12**
   - Download: https://www.python.org/downloads/
   - ✅ Centang "Add Python to PATH" saat install

2. **pip** (biasanya sudah include dengan Python)

3. **Git** (optional, untuk clone)
   - Download: https://git-scm.com/downloads

---

## 🚀 3 Langkah Setup

### 1️⃣ Clone Repo
```powershell
git clone https://github.com/gracesiana/Web-EyeDetect.git
cd Web-EyeDetect
```

### 2️⃣ Setup (Install Dependencies)
```powershell
.\setup.ps1
```
⏱️ Tunggu 5-10 menit. Script ini akan:
- Buat virtual environment
- Download & install **45+ packages** (~500 MB)
- Setup database
- Buat admin user

### 3️⃣ Run Server
```powershell
.\run.ps1
```
Buka browser: http://localhost:8000

---

## 📦 Apa Saja yang Diinstall?

Script akan menginstall dependencies ini:

| Package | Version | Size | Kegunaan |
|---------|---------|------|----------|
| Django | 6.0.7 | ~10 MB | Web framework |
| TensorFlow | 2.18.0 | ~350 MB | AI/Deep learning |
| OpenCV | Latest | ~50 MB | Image processing |
| Pillow | 11.2.1 | ~3 MB | Image library |
| NumPy | 1.26.4 | ~15 MB | Numerical computing |
| + 40 packages lainnya | - | ~50 MB | Support libraries |

**TOTAL: ~450-500 MB**

---

## 🔐 Login Info

**Admin:**
- URL: http://localhost:8000/login/admin/
- Username: `admin`
- Password: `admin123`

**User:** Daftar di http://localhost:8000/daftar/

---

## ⚠️ Troubleshooting Cepat

### "Scripts disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Python not found"
Reinstall Python dengan centang "Add to PATH"

### "ModuleNotFoundError"
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📖 Dokumentasi Lengkap

- 📘 [README.md](./README.md) - Overview project
- 📗 [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md) - Panduan install detail
- 📙 [DEPENDENCIES.md](./DEPENDENCIES.md) - List semua dependencies
- 📕 [CARA_MENJALANKAN.md](./CARA_MENJALANKAN.md) - Cara run setelah setup

---

**That's it! Simple as 1-2-3** 🎉
