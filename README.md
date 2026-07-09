# 👁️ EyeDetect - AI-Powered Eye Disease Detection

Platform deteksi penyakit mata berbasis AI menggunakan Deep Learning (CNN dengan MobileNetV2) untuk mendeteksi:
- 🔴 **Cataract** (Katarak)
- 🟢 **Glaucoma** (Glaukoma)
- 🔵 **Diabetic Retinopathy** (Retinopati Diabetik)
- ⚪ **Normal** (Mata Sehat)

---

## 🚀 Features

### 🤖 AI & Deep Learning
- **Model**: MobileNetV2 + Custom Classification Head
- **Accuracy**: Trained on large retina image dataset
- **XAI**: Grad-CAM visualization untuk explainability
- **Fast Prediction**: ~2-5 detik per image

### 👥 User Features
- ✅ User Registration & Authentication
- ✅ Upload & Analyze Retina Images
- ✅ Detection History & Statistics
- ✅ Detailed AI Explanation (XAI)
- ✅ Profile Management
- ✅ FAQ & Documentation

### 🔧 Admin Panel
- ✅ Dataset Management
- ✅ User Management
- ✅ Prediction History Monitoring
- ✅ Model Performance Tracking
- ✅ Activity Logs

---

## 🛠️ Tech Stack

### Backend
- **Django 6.0.7** - Web Framework
- **TensorFlow 2.18.0** - Deep Learning
- **PostgreSQL** - Database (Production)
- **SQLite** - Database (Development)
- **Gunicorn** - WSGI Server
- **WhiteNoise** - Static Files
- **Cloudinary** - Image Storage (Cloud)

### Frontend
- **HTML5 / CSS3** - UI Structure
- **JavaScript (Vanilla)** - Interactions
- **Bootstrap 5.3** - CSS Framework
- **Font Awesome 6.5** - Icons

### AI/ML
- **MobileNetV2** - Feature Extraction
- **Keras/TensorFlow** - Model Training
- **OpenCV** - Image Processing
- **Grad-CAM** - Explainable AI

---

## 📦 Installation

### Prerequisites
- Python 3.12+
- pip
- Git

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/gracesiana/Web-EyeDetect.git
cd Web-EyeDetect/backend
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and set:
# DJANGO_SECRET_KEY=your-secret-key-here
# DJANGO_DEBUG=True
# DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Run Migrations**
```bash
python manage.py migrate
```

6. **Create Admin User**
```bash
python manage.py ensure_default_admin
# Default credentials:
# Username: admin
# Password: admin123
```

7. **Run Development Server**
```bash
python manage.py runserver
```

8. **Access Application**
- Landing Page: http://localhost:8000/
- User Login: http://localhost:8000/login/
- Admin Login: http://localhost:8000/login/admin/
- Django Admin: http://localhost:8000/admin/

---

## 🚢 Deployment

### Deploy to Railway (Recommended)

**Langkah lengkap ada di**: [`RAILWAY_DEPLOYMENT.md`](./RAILWAY_DEPLOYMENT.md)

**Quick Steps:**
1. Push code ke GitHub
2. Buat akun di https://railway.app
3. Create New Project → Deploy from GitHub
4. Set Root Directory: `backend`
5. Add PostgreSQL database
6. Set Environment Variables
7. Deploy! ✅

**Railway Free Tier:**
- $5 credit/bulan (~500 jam)
- PostgreSQL included
- Auto SSL certificate
- Perfect untuk Django + AI model

---

## 🔐 Default Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@retinadetect.local`

### Staff Account
- **Username**: `jolie@eyedetect.com`
- **Password**: `staff123`
- **Email**: `jolie@eyedetect.com`

⚠️ **PENTING**: Ganti password setelah deployment pertama!

---

## 📁 Project Structure

```
Web-EyeDetect/
├── backend/                      # Django Backend
│   ├── ai_model/                # AI Model & Prediction
│   │   ├── eye_disease_model.h5 # Trained Model
│   │   ├── predict.py           # Prediction Logic
│   │   ├── gradcam.py           # Grad-CAM XAI
│   │   └── train.py             # Training Script
│   ├── appdeteksi/              # Main Django App
│   │   ├── models.py            # Database Models
│   │   ├── management/          # Custom Commands
│   │   └── migrations/          # DB Migrations
│   ├── EyeDetect/               # Project Settings
│   │   ├── settings.py          # Django Settings
│   │   ├── urls.py              # URL Routing
│   │   ├── views.py             # Main Views
│   │   ├── views_modules/       # Modular Views
│   │   │   ├── auth.py          # Authentication
│   │   │   ├── user.py          # User Features
│   │   │   └── admin.py         # Admin Panel
│   │   └── helpers/             # Helper Functions
│   ├── media/                   # Uploaded Images
│   ├── staticfiles/             # Static Files (Production)
│   ├── requirements.txt         # Python Dependencies
│   ├── Procfile                 # Railway/Heroku Config
│   ├── runtime.txt              # Python Version
│   ├── start.sh                 # Startup Script
│   └── manage.py                # Django Management
├── frontend/                    # Frontend Templates
│   ├── user/                    # User Templates
│   │   ├── welcome.html         # Landing Page
│   │   ├── login.html           # Login Page
│   │   ├── dashboard.html       # User Dashboard
│   │   ├── deteksi.html         # Detection Page
│   │   └── ...
│   ├── admin/                   # Admin Templates
│   │   ├── admin_dashboard.html # Admin Dashboard
│   │   ├── admin_dataset.html   # Dataset Management
│   │   └── ...
│   └── component/               # Static Assets
│       ├── images/              # Images
│       └── admin/               # Admin Assets
├── RAILWAY_DEPLOYMENT.md        # Railway Deploy Guide
├── DEPLOYMENT_GUIDE.md          # General Deploy Info
└── README.md                    # This file
```

---

## 🎯 Usage

### For Users

1. **Register Account**: Klik "Daftar" di halaman login
2. **Login**: Masuk dengan email & password
3. **Upload Image**: Pergi ke "Mulai Deteksi"
4. **View Results**: Lihat hasil prediksi + Grad-CAM visualization
5. **Check History**: Lihat riwayat deteksi di "Riwayat Skrining"

### For Admins

1. **Login Admin**: Akses `/login/admin/`
2. **Manage Users**: Monitor & manage user accounts
3. **View Predictions**: Monitor semua deteksi yang dilakukan
4. **Dataset Management**: Upload & manage training dataset
5. **Activity Logs**: Track system activities

---

## 🧪 Model Training

Model sudah di-train dan tersimpan di `backend/ai_model/eye_disease_model.h5`.

Jika ingin re-train:

```bash
cd backend/ai_model
python train.py
```

**Dataset Requirements:**
- Format: JPG/PNG images
- Structure:
  ```
  dataset/
  ├── train/
  │   ├── cataract/
  │   ├── glaucoma/
  │   ├── diabetic_retinopathy/
  │   └── normal/
  └── test/
      ├── cataract/
      ├── glaucoma/
      ├── diabetic_retinopathy/
      └── normal/
  ```

---

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Error: Database not found
```bash
python manage.py migrate
```

### Error: Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Error: Model file not found
Pastikan `ai_model/eye_disease_model.h5` ada di folder yang benar.

---

## 📊 Model Performance

- **Accuracy**: ~85-90% (depending on dataset quality)
- **Classes**: 4 (Cataract, Glaucoma, Diabetic Retinopathy, Normal)
- **Input Size**: 224x224 RGB
- **Architecture**: MobileNetV2 (transfer learning)
- **Training Time**: ~2-4 hours on GPU

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Author

**Grace Siana**
- GitHub: [@gracesiana](https://github.com/gracesiana)
- Repository: [Web-EyeDetect](https://github.com/gracesiana/Web-EyeDetect)

---

## 🙏 Acknowledgments

- Dataset: Public retina image datasets
- Framework: Django, TensorFlow, MobileNetV2
- Inspiration: AI-powered healthcare solutions

---

## 📞 Support

Jika ada pertanyaan atau issue:
1. Buka [GitHub Issues](https://github.com/gracesiana/Web-EyeDetect/issues)
2. Email: (your-email@example.com)

---

**Made with ❤️ for better eye health screening**
