# ▶️ Cara Menjalankan EyeDetect

Panduan singkat untuk menjalankan server setelah setup selesai.

> 📦 Belum setup? Baca dulu [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md)

---

## 🚀 Cara Paling Mudah

Dari folder root project, jalankan:

```powershell
.\run.ps1
```

Buka browser ke **http://localhost:8000** ✅

---

## 🔧 Cara Manual

Jika ingin jalankan manual:

```powershell
# 1. Masuk ke folder backend
cd backend

# 2. Aktifkan virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Jalankan server
python manage.py runserver
```

---

## 🌐 URL Penting

| Halaman | URL |
|---------|-----|
| Landing Page | http://localhost:8000/ |
| Login User | http://localhost:8000/login/ |
| Login Admin | http://localhost:8000/login/admin/ |
| Dashboard User | http://localhost:8000/dashboard/ |
| Panel Admin | http://localhost:8000/admin-panel/ |
| Django Admin | http://localhost:8000/admin/ |

---

## 🔐 Akun Default

### Admin
- URL: http://localhost:8000/login/admin/
- Username: `admin`
- Password: `admin123`

### User Biasa
- Daftar di: http://localhost:8000/daftar/

---

## 🛑 Stop Server

Tekan **CTRL + C** di terminal.

---

## 🔄 Setiap Kali Ingin Run

Setelah setup pertama, tiap kali mau run:

```powershell
# Dari root folder
.\run.ps1
```

Atau manual:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## ⚠️ Troubleshooting Cepat

### Port 8000 sudah dipakai
```powershell
python manage.py runserver 8080
```

### "Scripts disabled" error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "ModuleNotFoundError"
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Static files tidak muncul
```powershell
python manage.py collectstatic --noinput
```

---

## 📖 Dokumentasi Lainnya

- ⚡ [QUICK_START.md](./QUICK_START.md) — Setup 3 langkah untuk kontributor baru
- 📗 [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md) — Panduan install lengkap
- 📦 [DEPENDENCIES.md](./DEPENDENCIES.md) — Daftar semua dependencies
- ✅ [CONTRIBUTOR_CHECKLIST.md](./CONTRIBUTOR_CHECKLIST.md) — Checklist development

---

**EyeDetect — AI-Powered Eye Disease Detection** 👁️
