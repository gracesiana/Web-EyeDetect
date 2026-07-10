# ✅ Checklist untuk Kontributor

Gunakan checklist ini untuk memastikan environment Anda siap untuk development.

---

## 📋 Pre-Installation Checklist

Sebelum clone & setup:

- [ ] **Python 3.10/3.11/3.12** sudah terinstall
  - Cek: `python --version` atau `py --version`
  - Download: https://www.python.org/downloads/
  
- [ ] **Python sudah di PATH**
  - Coba: `python` di terminal harus jalan
  - Jika belum: Reinstall Python dengan centang "Add to PATH"

- [ ] **pip** tersedia
  - Cek: `pip --version`
  - Fix: `python -m ensurepip --upgrade`

- [ ] **Internet stabil** (~500 MB akan didownload)

- [ ] **Disk space** minimal 2 GB free space

- [ ] **Git** terinstall (optional)
  - Cek: `git --version`
  - Download: https://git-scm.com/downloads

---

## 📥 Installation Checklist

Setelah clone repo:

- [ ] Repository sudah di-clone atau di-download
  ```powershell
  git clone https://github.com/gracesiana/Web-EyeDetect.git
  ```

- [ ] Sudah masuk ke folder project
  ```powershell
  cd Web-EyeDetect
  ```

- [ ] **Setup script berhasil dijalankan**
  ```powershell
  .\setup.ps1
  ```

- [ ] Virtual environment dibuat (folder `.venv` ada di `backend/`)
  ```powershell
  Test-Path backend\.venv
  # Harus return: True
  ```

- [ ] Dependencies terinstall (45+ packages)
  ```powershell
  cd backend
  .\.venv\Scripts\Activate.ps1
  pip list
  # Harus ada: Django, tensorflow, opencv-python-headless, dll
  ```

- [ ] Database sudah di-migrate (file `db.sqlite3` ada di `backend/`)
  ```powershell
  Test-Path backend\db.sqlite3
  # Harus return: True
  ```

- [ ] Admin user sudah dibuat
  - Username: `admin`
  - Password: `admin123`

---

## 🚀 Running Checklist

Sebelum mulai development:

- [ ] **Server bisa running**
  ```powershell
  .\run.ps1
  # Atau manual:
  cd backend
  .\.venv\Scripts\Activate.ps1
  python manage.py runserver
  ```

- [ ] **Landing page bisa dibuka**
  - Buka browser: http://localhost:8000/
  - Harus muncul halaman welcome

- [ ] **Login admin berhasil**
  - URL: http://localhost:8000/login/admin/
  - Username: `admin`
  - Password: `admin123`

- [ ] **Dashboard admin bisa diakses**
  - http://localhost:8000/admin-panel/

- [ ] **Deteksi image berfungsi**
  - Upload gambar mata di menu "Mulai Deteksi"
  - Harus muncul hasil prediksi

- [ ] **Static files loading**
  - CSS, JS, images harus muncul dengan benar
  - Tidak ada error di browser console

---

## 🧪 Development Checklist

Sebelum mulai coding:

- [ ] **Virtual environment aktif** (ada `(.venv)` di terminal)
  ```powershell
  cd backend
  .\.venv\Scripts\Activate.ps1
  ```

- [ ] **Editor/IDE sudah setup**
  - Recommended: VS Code, PyCharm
  - Python interpreter di-set ke `.venv`

- [ ] **Git branch untuk feature baru**
  ```bash
  git checkout -b feature/nama-fitur
  ```

- [ ] **Model AI ada** (file `eye_disease_model.h5` ~9 MB)
  ```powershell
  Test-Path backend\ai_model\eye_disease_model.h5
  ```

---

## 🐛 Troubleshooting Checklist

Jika ada masalah:

- [ ] **Python version correct?**
  ```powershell
  python --version
  # Harus: 3.10.x atau 3.11.x atau 3.12.x
  ```

- [ ] **Virtual environment aktif?**
  - Lihat `(.venv)` di awal baris terminal

- [ ] **Dependencies lengkap?**
  ```powershell
  pip list | Select-String "Django|tensorflow|opencv"
  ```

- [ ] **Database sudah migrate?**
  ```powershell
  python manage.py migrate
  ```

- [ ] **Port 8000 tersedia?**
  - Tidak ada aplikasi lain yang pakai port 8000
  - Atau run di port lain: `python manage.py runserver 8080`

- [ ] **Execution Policy issue?**
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- [ ] **Restart terminal?**
  - Kadang perlu restart setelah install Python

---

## 📦 Dependency Verification

Cek package-package penting:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1

# Cek Django
python -c "import django; print(django.get_version())"
# Output: 6.0.7

# Cek TensorFlow
python -c "import tensorflow as tf; print(tf.__version__)"
# Output: 2.18.0 atau 2.21.0

# Cek OpenCV
python -c "import cv2; print(cv2.__version__)"
# Output: 4.x.x atau 5.x.x

# Cek Pillow
python -c "from PIL import Image; print(Image.__version__)"
# Output: 11.2.1

# Cek NumPy
python -c "import numpy; print(numpy.__version__)"
# Output: 1.26.4 atau 2.x.x
```

Semua harus berhasil tanpa error!

---

## 🎯 Final Verification

Sebelum mulai kontribusi, pastikan:

- [ ] ✅ Environment sudah setup sempurna
- [ ] ✅ Server bisa running tanpa error
- [ ] ✅ Semua fitur utama berfungsi
- [ ] ✅ Bisa login sebagai admin dan user
- [ ] ✅ Bisa upload dan detect image
- [ ] ✅ Git sudah dikonfigurasi (name & email)

---

## 📊 Summary

| Item | Status | Notes |
|------|--------|-------|
| Python 3.10+ | ⬜ | Cek: `python --version` |
| pip | ⬜ | Cek: `pip --version` |
| Repo cloned | ⬜ | Folder `Web-EyeDetect` ada |
| Setup done | ⬜ | Jalankan `.\setup.ps1` |
| `.venv` created | ⬜ | Folder ada di `backend/` |
| Dependencies installed | ⬜ | 45+ packages |
| Database migrated | ⬜ | File `db.sqlite3` ada |
| Admin created | ⬜ | admin/admin123 |
| Server running | ⬜ | http://localhost:8000 |
| Ready to code | ⬜ | 🎉 |

---

## 🤝 Butuh Bantuan?

Jika checklist di atas ada yang gagal:

1. 📖 Baca [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md)
2. 🔍 Cek bagian Troubleshooting
3. 🐛 Buat issue di GitHub
4. 📧 Kontak maintainer

---

**Happy Contributing! 🚀**
