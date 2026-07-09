# ⚡ QUICKSTART: Deploy ke Railway

## ✅ Yang Sudah Siap di Repository:

1. ✅ `backend/requirements.txt` - Semua dependencies lengkap (Django, TensorFlow, Gunicorn, dll)
2. ✅ `backend/Procfile` - Railway startup command
3. ✅ `backend/runtime.txt` - Python 3.12.4
4. ✅ `backend/start.sh` - Migration, admin setup, collectstatic
5. ✅ `backend/nixpacks.toml` - Railway build config
6. ✅ `backend/.env.example` - Template environment variables
7. ✅ `backend/EyeDetect/settings.py` - Production-ready settings

**Repository Anda SIAP untuk Railway! 🚀**

---

## 🎯 5 LANGKAH DEPLOY (15 Menit)

### 1. Login Railway
- Buka: https://railway.app
- Klik **"Login with GitHub"**

### 2. Create Project
- Dashboard → **"+ New Project"**
- **"Deploy from GitHub repo"**
- Pilih: **`gracesiana/Web-EyeDetect`**

### 3. Set Root Directory
- Klik service name
- Tab **"Settings"**
- **"Root Directory"** → `backend`
- **"Update"**

### 4. Add PostgreSQL
- Dashboard → **"+ New"**
- **"Database"** → **"PostgreSQL"**

### 5. Set Variables
Tab **"Variables"** → Add:

```
DJANGO_SECRET_KEY=<generate di https://djecrety.ir/>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app
DJANGO_SECURE_SSL_REDIRECT=True
```

**Deploy otomatis setelah set variables!** ✅

---

## 🔐 Login Setelah Deploy

### Admin
- URL: `https://your-app.railway.app/login/admin/`
- Username: `admin`
- Password: `admin123`

### User Baru
- Daftar di: `https://your-app.railway.app/daftar/`

---

## ✅ Yang Akan Otomatis Berjalan:

1. ✅ Install Python & dependencies (5-10 menit pertama kali)
2. ✅ Database migration otomatis
3. ✅ Create default admin account
4. ✅ Collect static files (CSS, JS, images)
5. ✅ Start Gunicorn server
6. ✅ Connect PostgreSQL database

**Tidak perlu konfigurasi tambahan!**

---

## 🎉 Selesai!

Aplikasi live di: `https://web-eyedetect-production.up.railway.app`

**Test:**
- Landing page
- Login user
- Upload gambar retina
- Lihat hasil deteksi + Grad-CAM
- Check admin panel

---

## 📊 Free Tier Railway

- **$5 credit/bulan** (~500 jam)
- **PostgreSQL included**
- **Auto SSL certificate**
- **Perfect untuk TensorFlow apps**

---

**Butuh bantuan? Open issue di GitHub!** 💪
