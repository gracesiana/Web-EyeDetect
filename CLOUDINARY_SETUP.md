# 🌥️ Cloudinary Setup untuk EyeDetect

## Kenapa Butuh Cloudinary?

Railway menggunakan **ephemeral filesystem** - artinya semua file yang di-upload akan **hilang** setiap kali app restart/redeploy.

Cloudinary adalah **cloud storage** untuk menyimpan gambar secara permanen:
- ✅ Gambar uploaded user
- ✅ Grad-CAM heatmap hasil AI
- ✅ Profile pictures
- ✅ Dataset samples (opsional)

---

## 📋 Step 1: Buat Akun Cloudinary (GRATIS)

1. **Buka**: https://cloudinary.com/users/register_free
2. **Sign up** dengan email Anda
3. **Verify email** Anda
4. **Login** ke Cloudinary Console

**Free Tier Benefits:**
- ✅ 25 GB storage
- ✅ 25 GB bandwidth per bulan
- ✅ Unlimited transformations
- ✅ Perfect untuk aplikasi EyeDetect

---

## 📋 Step 2: Dapatkan Credentials

Setelah login ke Cloudinary Dashboard:

1. Buka **Dashboard** → https://cloudinary.com/console
2. Lihat bagian **"Account Details"** atau **"Product Environment Credentials"**
3. Anda akan melihat:

```
Cloud Name: your-cloud-name
API Key: 123456789012345
API Secret: abcdefghijklmnopqrstuvwxyz
```

**PENTING**: 
- ⚠️ Jangan share **API Secret** dengan siapapun
- ⚠️ Simpan credentials ini untuk Step 3

---

## 📋 Step 3: Setup di Railway

### 3.1 Buka Railway Dashboard

1. Login ke **https://railway.app**
2. Pilih project **Web-EyeDetect**
3. Klik service **web**

### 3.2 Tambah Environment Variables

Klik tab **"Variables"** → **"+ New Variable"**

Tambahkan 3 variables ini:

#### Variable 1:
```
Name:  CLOUDINARY_CLOUD_NAME
Value: your-cloud-name
```
(Ganti `your-cloud-name` dengan Cloud Name dari Cloudinary)

#### Variable 2:
```
Name:  CLOUDINARY_API_KEY
Value: 123456789012345
```
(Ganti dengan API Key Anda)

#### Variable 3:
```
Name:  CLOUDINARY_API_SECRET
Value: abcdefghijklmnopqrstuvwxyz
```
(Ganti dengan API Secret Anda)

### 3.3 Redeploy

Setelah tambah 3 variables:
1. Railway akan **otomatis redeploy**
2. Atau klik **"Redeploy"** manual
3. Tunggu build selesai (~5-10 menit)

---

## ✅ Step 4: Verifikasi Setup

### 4.1 Test Upload Gambar

1. Buka aplikasi Railway Anda: `https://your-app.railway.app`
2. **Login** dengan akun user
3. Pergi ke **"Mulai Deteksi"**
4. **Upload gambar retina**
5. Tunggu hasil analisis

### 4.2 Cek di Cloudinary

1. Buka **Cloudinary Console** → **Media Library**
2. Anda akan melihat:
   - Folder **`detections/`** - gambar uploaded user
   - Folder **`gradcam/`** - heatmap AI
   - Folder **`profile_images/`** - foto profil (jika ada)

### 4.3 Test di Riwayat Skrining

1. Buka menu **"Riwayat Skrining"**
2. Lihat card screening Anda
3. **Gambar INPUT dan HEATMAP seharusnya MUNCUL** ✅

---

## 🔍 Troubleshooting

### ❌ Error: "Cloudinary credentials not configured"

**Penyebab**: Environment variables belum diset di Railway

**Solusi**:
1. Cek Railway → Variables tab
2. Pastikan ada 3 variables: `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
3. Pastikan tidak ada typo di nama variable
4. Redeploy aplikasi

---

### ❌ Error: "Invalid Cloudinary credentials"

**Penyebab**: Credentials salah atau expired

**Solusi**:
1. Login ke Cloudinary Console
2. Dashboard → Cek credentials
3. Copy-paste ulang ke Railway variables
4. Pastikan tidak ada spasi di awal/akhir value

---

### ❌ Gambar masih tidak muncul

**Penyebab**: 
1. Build Railway belum selesai
2. Old deployments masih running
3. Browser cache

**Solusi**:
1. Tunggu deployment selesai (check logs)
2. Hard refresh browser: `Ctrl + Shift + R` (Windows) atau `Cmd + Shift + R` (Mac)
3. Coba di incognito/private window
4. Cek Railway logs untuk error messages

---

### ❌ Upload error: "Upload failed"

**Penyebab**: File terlalu besar atau format tidak support

**Solusi**:
1. Pastikan file gambar < 10MB
2. Format support: JPG, PNG, JPEG
3. Coba compress gambar dulu
4. Check Railway logs untuk detail error

---

## 📊 Monitor Usage

### Cek Cloudinary Usage:

1. **Dashboard** → **"Usage"** tab
2. Monitor:
   - **Storage**: Berapa GB terpakai (limit 25GB)
   - **Bandwidth**: Transfer data bulan ini (limit 25GB)
   - **Transformations**: Image processing (unlimited)

### Tips Hemat Quota:

✅ **Compress images** sebelum upload  
✅ **Set auto-format** di Cloudinary untuk optimize  
✅ **Delete old test images** yang tidak diperlukan  
✅ **Enable caching** di browser untuk reduce bandwidth  

---

## 🎯 Hasil Akhir

Setelah setup Cloudinary berhasil:

✅ **User upload gambar** → Tersimpan di Cloudinary  
✅ **AI generate Grad-CAM** → Tersimpan di Cloudinary  
✅ **Riwayat skrining** → Gambar INPUT & HEATMAP muncul  
✅ **Profile picture** → Tersimpan permanen  
✅ **App restart** → Gambar tetap ada (tidak hilang)  

---

## 📞 Bantuan

Jika masih ada masalah:

1. **Cek Railway Logs**:
   - Railway Dashboard → Deployments tab → View Logs
   - Cari error message dengan keyword "cloudinary"

2. **Cek Cloudinary Logs**:
   - Cloudinary Console → Activity tab
   - Lihat upload attempts dan errors

3. **GitHub Issues**:
   - Buka issue di repository
   - Attach screenshot error dan logs

---

**Setup Complete! 🎉**

Aplikasi EyeDetect Anda sekarang menggunakan Cloudinary untuk persistent image storage!
