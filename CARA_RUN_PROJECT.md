# 🚀 Cara Run Project EyeDetect - Lokal Development

## 📋 Prerequisites (Yang Harus Diinstall Dulu)

### 1. Install Python
- Download Python 3.10 atau 3.11 atau 3.12 dari: https://www.python.org/downloads/
- Saat install, **WAJIB centang "Add Python to PATH"**
- Verifikasi instalasi:
  ```powershell
  python --version
  ```
  atau
  ```powershell
  py --version
  ```

---

## 🛠️ Langkah-Langkah Setup Project

### **1. Clone/Download Project**
Jika belum punya projectnya, clone dari GitHub:
```powershell
git clone https://github.com/gracesiana/Web-EyeDetect.git
cd Web-EyeDetect
```

Atau jika sudah ada, masuk ke folder project:
```powershell
cd D:\web-eyedetect\Web-EyeDetect
```

---

### **2. Masuk ke Folder Backend**
```powershell
cd backend
```

---

### **3. Buat Virtual Environment**
```powershell
python -m venv .venv
```

atau jika ada multiple Python versions:
```powershell
py -m venv .venv
```

---

### **4. Aktifkan Virtual Environment**

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

**Git Bash:**
```bash
source .venv/Scripts/activate
```

Setelah aktif, akan muncul `(.venv)` di awal baris command.

---

### **5. Upgrade pip**
```powershell
python -m pip install --upgrade pip
```

---

### **6. Install Dependencies**

**Opsi 1: Install dari requirements.txt**
```powershell
pip install -r ..\requirements.txt
```

**Opsi 2: Install Manual (jika requirements.txt error)**
```powershell
pip install Django==6.0.7
pip install whitenoise==6.12.0
pip install Pillow==11.2.1
pip install numpy
pip install tensorflow
pip install opencv-python-headless
pip install cloudinary==1.41.0
pip install django-cloudinary-storage==0.3.0
pip install psycopg[binary]==3.2.1
pip install gunicorn==23.0.0
```

---

### **7. Setup Environment Variables (Optional untuk Development)**

Copy file `.env.example` ke `.env`:
```powershell
copy .env.example .env
```

Edit `.env` (minimal untuk local development):
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

**Note:** Untuk local development, file `.env` tidak wajib. Django akan pakai SQLite dan settings default.

---

### **8. Jalankan Database Migration**
```powershell
python manage.py migrate
```

---

### **9. Buat Admin User**
```powershell
python manage.py ensure_default_admin
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

---

### **10. Run Development Server** 🚀
```powershell
python manage.py runserver
```

Server akan jalan di: **http://127.0.0.1:8000/**

---

## 🌐 URL yang Bisa Diakses

- **Landing Page**: http://localhost:8000/
- **User Login**: http://localhost:8000/login/
- **Admin Login**: http://localhost:8000/login/admin/
- **Django Admin Panel**: http://localhost:8000/admin/

---

## 🔐 Default User Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@retinadetect.local`
- **Akses**: Full admin access

### Staff Account (Testing)
- **Username**: `jolie@eyedetect.com`
- **Password**: `staff123`
- **Email**: `jolie@eyedetect.com`
- **Akses**: Staff level access

---

## 🔄 Cara Run Project Selanjutnya (Setelah Setup Pertama)

Setiap kali mau run project lagi, cukup:

```powershell
# 1. Masuk ke folder backend
cd D:\web-eyedetect\Web-EyeDetect\backend

# 2. Aktifkan virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Run server
python manage.py runserver
```

---

## 🛑 Cara Stop Server

Tekan **CTRL + C** di terminal untuk stop server.

---

## 🐛 Troubleshooting

### Error: "Python was not found"
**Solusi:** Install Python dan pastikan sudah di-add ke PATH.

### Error: "Activate.ps1 cannot be loaded"
**Solusi:** Jalankan di PowerShell sebagai Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "No module named 'django'"
**Solusi:** 
1. Pastikan virtual environment sudah aktif (ada `(.venv)` di command line)
2. Install ulang dependencies:
   ```powershell
   pip install Django==6.0.7
   ```

### Error: "No module named 'tensorflow'"
**Solusi:** Install TensorFlow:
```powershell
pip install tensorflow
```

**Note:** TensorFlow kadang butuh waktu lama untuk download (file besar ~350MB).

### Error: Static files tidak loading
**Solusi:**
```powershell
python manage.py collectstatic --noinput
```

### Error: Model file not found
**Solusi:** Pastikan file `ai_model/eye_disease_model.h5` ada di folder `backend/ai_model/`.

### Port 8000 sudah dipakai
**Solusi:** Jalankan di port lain:
```powershell
python manage.py runserver 8080
```

---

## 📦 Struktur Project

```
Web-EyeDetect/
├── backend/                      # Django Backend
│   ├── .venv/                    # Virtual Environment (dibuat saat setup)
│   ├── ai_model/                 # AI Model & Prediction
│   │   └── eye_disease_model.h5  # Trained Model
│   ├── appdeteksi/               # Main Django App
│   ├── EyeDetect/                # Project Settings
│   ├── media/                    # Uploaded Images (dibuat otomatis)
│   ├── db.sqlite3                # Database (dibuat otomatis)
│   └── manage.py                 # Django Management Script
├── frontend/                     # Frontend Templates
├── requirements.txt              # Python Dependencies
└── README.md                     # Dokumentasi Project
```

---

## 📝 Catatan Penting

1. **Virtual Environment Wajib**: Selalu aktifkan `.venv` sebelum run project.
2. **Database**: Project ini pakai SQLite untuk development (otomatis dibuat).
3. **Media Files**: Upload images disimpan di folder `backend/media/`.
4. **AI Model**: Model TensorFlow harus ada di `backend/ai_model/eye_disease_model.h5`.
5. **Development Server**: Jangan pakai untuk production. Untuk production pakai Gunicorn + PostgreSQL.

---

## ✅ Checklist Setup

- [ ] Python terinstall
- [ ] Virtual environment dibuat
- [ ] Virtual environment aktif (ada `.venv` di command line)
- [ ] Dependencies terinstall
- [ ] Database migration selesai
- [ ] Admin user dibuat
- [ ] Server running di http://localhost:8000/

---

## 🎯 Next Steps

Setelah server jalan:
1. Buka browser ke http://localhost:8000/
2. Register akun user atau login dengan admin account
3. Upload gambar retina untuk deteksi
4. Lihat hasil prediksi + Grad-CAM visualization

---

## 📞 Need Help?

Jika ada error atau masalah:
1. Pastikan semua langkah di atas sudah diikuti
2. Check error message di terminal
3. Google error message untuk solusi
4. Check GitHub Issues: https://github.com/gracesiana/Web-EyeDetect/issues

---

**Made with ❤️ - EyeDetect Team**
