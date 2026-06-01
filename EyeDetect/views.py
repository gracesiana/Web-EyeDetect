import math
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from urllib3 import request

from ai_model.predict import predict_image
from ai_model.gradcam import generate_gradcam
from appdeteksi.models import DetectionHistory


def welcome(request):
    return render(request, 'welcome.html')


def show_login(request):
    return render(request, 'login.html')


def show_admin_login(request):
    return render(request, 'admin_login.html')


def login_proses(request):
    if request.method != 'POST':
        return redirect('login')

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    # Check if the user requested admin login
    login_as_admin = bool(request.POST.get('login_as_admin'))

    if not email or not password:
        messages.error(request, 'Email dan password harus diisi.')
        return render(request, 'admin_login.html' if login_as_admin else 'login.html')

    # Check if the user requested admin login
    

    # First try authenticating with the entered value as username.
    user = authenticate(request, username=email, password=password)
    if user is None:
        # If that failed, try matching the email field to a User.
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

    if user is not None:
        # If admin-login was requested, ensure the account is staff/superuser
        if login_as_admin and not (user.is_staff or user.is_superuser):
            messages.error(request, 'Akun ini bukan akun admin.')
            return render(request, 'admin_login.html')

        login(request, user)
        # Redirect admin/staff users to the admin panel, regular users to the dashboard
        if user.is_staff or user.is_superuser:
            return redirect('admin_panel')
        return redirect('dashboard')

    messages.error(request, 'Email atau password tidak valid.')
    return render(request, 'admin_login.html' if login_as_admin else 'login.html')


def show_daftar(request):
    return render(request, 'daftar.html')


def daftar_proses(request):
    if request.method != 'POST':
        return redirect('register')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    password_confirmation = request.POST.get('password_confirmation', '')

    if not name or not email or not password or not password_confirmation:
        messages.error(request, 'Semua kolom harus diisi.')
        return render(request, 'daftar.html')

    if password != password_confirmation:
        messages.error(request, 'Password dan konfirmasi password tidak sama.')
        return render(request, 'daftar.html')

    if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
        messages.error(request, 'Email ini sudah terdaftar. Silakan gunakan email lain.')
        return render(request, 'daftar.html')

    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name = name
    user.save()

    messages.success(request, 'Registrasi berhasil. Silakan login.')
    return redirect('login')

def lupa_password(request):
    # Add logic for password recovery here
    return render(request, 'lupa-password.html')

def logout_user(request):
    # Allow logout via GET or POST — uses same logout for admin and regular users
    logout(request)
    return redirect('login')


def dashboard(request):
    screening_count = 0
    return render(request, 'dashboard.html', {
        'screeningCount': screening_count,
    })

from django.core.files.storage import FileSystemStorage

def deteksi(request):

    print("METHOD:", request.method)

    hasil = None
    confidence = None
    filename = None
    gradcam_image = None

    if request.method == "POST":

        print("POST MASUK")

        retina_image = request.FILES.get("retina_image")

        print("FILE:", retina_image)

        if retina_image:

            fs = FileSystemStorage()

            filename = fs.save(
                retina_image.name,
                retina_image
            )

            filepath = fs.path(filename)

            print("FILEPATH:", filepath)

            hasil, confidence = predict_image(filepath)

            print("HASIL:", hasil)
            print("CONFIDENCE:", confidence)

            if request.user.is_authenticated:

                DetectionHistory.objects.create(
                    user=request.user,
                    image=filename,
                    result=hasil,
                    confidence=confidence
                )

            gradcam_filename = "gradcam_" + filename

            gradcam_path = fs.path(gradcam_filename)

            generate_gradcam(
                filepath,
                gradcam_path
            )

            gradcam_image = "/media/" + gradcam_filename

            print("HASIL:", hasil)
            print("CONFIDENCE:", confidence)

    return render(
    request,
    "deteksi.html",
    {
        "hasil": hasil,
        "confidence": confidence,
        "filename": filename,
        "gradcam_image": gradcam_image,
    }
)

def cara_kerja(request):
    return render(request, 'cara-kerja.html')

def profile(request):
    return render(request, 'profile.html')

def riwayat(request):
    screenings = []  # Placeholder untuk data screening user
    return render(request, 'riwayat-skrining.html', {
        'screenings': screenings,
    })

def pengaturan(request):
    return render(request, 'pengaturan.html')


def _get_admin_data():
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    new_users_last_week = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7)).count()

    stats = {
        'total_dataset': 1245,
        'total_predictions': 3482,
        'model_accuracy': '89.32%',
        'total_users': total_users,
        'active_users': active_users,
        'new_users_last_week': new_users_last_week,
    }

    latest_predictions = [
        {'id': 'PRD-3482', 'result': 'Glaukoma', 'confidence': 87, 'user': 'user123', 'date': '20 Mei 2026 14:32'},
        {'id': 'PRD-3481', 'result': 'Diabetic Retinopathy', 'confidence': 76, 'user': 'user456', 'date': '20 Mei 2026 14:20'},
        {'id': 'PRD-3480', 'result': 'Normal', 'confidence': 93, 'user': 'user789', 'date': '20 Mei 2026 14:05'},
        {'id': 'PRD-3479', 'result': 'Katarak', 'confidence': 81, 'user': 'user321', 'date': '20 Mei 2026 13:50'},
        {'id': 'PRD-3478', 'result': 'Glaukoma', 'confidence': 88, 'user': 'user654', 'date': '20 Mei 2026 13:41'},
      ]

    dataset_items = [
        {'id': 'DS-1245', 'image': 'https://images.unsplash.com/photo-1580281657528-843557120a72?auto=format&fit=crop&w=80&q=80', 'disease': 'Glaukoma', 'upload_date': '20 Mei 2026', 'size': '256 KB', 'status': 'Verified'},
        {'id': 'DS-1244', 'image': 'https://images.unsplash.com/photo-1515942401378-4847d02f31f3?auto=format&fit=crop&w=80&q=80', 'disease': 'Diabetic Retinopathy', 'upload_date': '20 Mei 2026', 'size': '312 KB', 'status': 'Verified'},
        {'id': 'DS-1243', 'image': 'https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=80&q=80', 'disease': 'Katarak', 'upload_date': '19 Mei 2026', 'size': '245 KB', 'status': 'Pending'},
        {'id': 'DS-1242', 'image': 'https://images.unsplash.com/photo-1485217988980-11786ced9454?auto=format&fit=crop&w=80&q=80', 'disease': 'Normal', 'upload_date': '19 Mei 2026', 'size': '198 KB', 'status': 'Verified'},
        {'id': 'DS-1241', 'image': 'https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=80&q=80', 'disease': 'Glaukoma', 'upload_date': '18 Mei 2026', 'size': '276 KB', 'status': 'Reviewed'},
        {'id': 'DS-1240', 'image': 'https://images.unsplash.com/photo-1495433324511-bf8e92934d90?auto=format&fit=crop&w=80&q=80', 'disease': 'Normal', 'upload_date': '18 Mei 2026', 'size': '212 KB', 'status': 'Verified'},
      ]

    model_info = {
        'name': 'RetinaNet Premium AI',
        'version': 'v3.1',
        'accuracy': '89.32%',
        'precision': '91.8%',
        'recall': '87.4%',
        'trained_at': '20 Mei 2026',
        'architecture': 'ResNet50 + DenseNet',
        'parameters': '24.8M',
        'status': 'Production',
    }

    model_history = [
        {'version': 'v3.1', 'accuracy': '89.32%', 'date': '20 Mei 2026', 'status': 'Production'},
        {'version': 'v3.0', 'accuracy': '88.01%', 'date': '15 Mei 2026', 'status': 'Staging'},
        {'version': 'v2.8', 'accuracy': '85.43%', 'date': '10 Mei 2026', 'status': 'Archive'},
      ]

    prediction_distribution = {
        'labels': ['Normal', 'Katarak', 'Glaukoma', 'Diabetic Retinopathy'],
        'values': [35, 21, 27, 17],
      }

    monthly_trend = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei'],
        'values': [320, 420, 380, 460, 520],
    }

    activity_logs = [
        {'time': '20 Mei 2026 14:35', 'action': 'User login', 'user': 'user123', 'status': 'Berhasil'},
        {'time': '20 Mei 2026 14:20', 'action': 'Prediksi baru dibuat', 'user': 'user456', 'status': 'Berhasil'},
        {'time': '20 Mei 2026 13:50', 'action': 'Dataset ditambahkan', 'user': 'admin', 'status': 'Berhasil'},
    ]

    users_list = [
        {'name': 'Andi Pratama', 'email': 'andi@example.com', 'status': 'Aktif', 'access': 'User'},
        {'name': 'Siti Aisyah', 'email': 'siti@example.com', 'status': 'Aktif', 'access': 'User'},
        {'name': 'Budi Santoso', 'email': 'budi@example.com', 'status': 'Nonaktif', 'access': 'User'},
    ]

    return {
        'stats': stats,
        'latest_predictions': latest_predictions,
        'dataset_items': dataset_items,
        'model_info': model_info,
        'model_history': model_history,
        'prediction_distribution': prediction_distribution,
        'monthly_trend': monthly_trend,
        'activity_logs': activity_logs,
        'users_list': users_list,
    }


def admin_dashboard(request):
    context = _get_admin_data()
    context.update({
        'page_title': 'Dashboard',
        'current_page': 'dashboard',
    })
    return render(request, 'admin_dashboard.html', context)


def admin_dataset(request):
    context = _get_admin_data()
    uploaded_items = request.session.get('uploaded_dataset_items', [])

    if request.method == 'POST':
        dataset_file = request.FILES.get('dataset_file')
        disease = request.POST.get('disease', '').strip()

        if not dataset_file or not disease:
            messages.error(request, 'Unggah file gambar dan pilih kelas penyakit.')
        else:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'dataset_uploads')
            os.makedirs(upload_dir, exist_ok=True)
            filename = f"{int(datetime.now().timestamp())}_{dataset_file.name}"
            filepath = os.path.join(upload_dir, filename)
            with open(filepath, 'wb') as f:
                for chunk in dataset_file.chunks():
                    f.write(chunk)

            file_url = f"{settings.MEDIA_URL}dataset_uploads/{filename}"
            new_item = {
                'id': f"DS-NEW-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'image': file_url,
                'disease': disease,
                'upload_date': datetime.now().strftime('%d %B %Y'),
                'size': f"{round(dataset_file.size / 1024)} KB",
                'status': 'Pending',
            }
            uploaded_items.insert(0, new_item)
            request.session['uploaded_dataset_items'] = uploaded_items
            messages.success(request, 'Dataset berhasil diunggah dan muncul di daftar.')

    search_query = request.GET.get('search', '').strip()
    combined_items = uploaded_items + context['dataset_items']
    if search_query:
        combined_items = [
            item for item in combined_items
            if search_query.lower() in item['id'].lower()
            or search_query.lower() in item['disease'].lower()
            or search_query.lower() in item['status'].lower()
        ]

    page = max(1, int(request.GET.get('page', 1)))
    page_size = 5
    total_pages = max(1, math.ceil(len(combined_items) / page_size))
    if page > total_pages:
        page = total_pages
    start = (page - 1) * page_size
    end = start + page_size

    context.update({
        'page_title': 'Dataset Retina',
        'current_page': 'dataset',
        'dataset_items': combined_items[start:end],
        'dataset_page': page,
        'dataset_total_pages': total_pages,
        'search_query': search_query,
    })
    return render(request, 'admin_dataset.html', context)


def admin_predictions(request):
    context = _get_admin_data()
    context.update({
        'page_title': 'Hasil Prediksi',
        'current_page': 'predictions',
    })
    return render(request, 'admin_predictions.html', context)


def admin_model_cnn(request):
    context = _get_admin_data()
    context.update({
        'page_title': 'Model CNN',
        'current_page': 'model',
    })
    return render(request, 'admin_model_cnn.html', context)


from django.contrib.auth.models import User

def admin_users(request):

    users = User.objects.all().order_by('-date_joined')

    return render(
        request,
        'admin_users.html',
        {
            'page_title': 'Pengguna',
            'current_page': 'users',
            'users': users,
            'total_users': users.count()
        }
    )


def admin_settings(request):
    context = _get_admin_data()
    context.update({
        'page_title': 'Pengaturan',
        'current_page': 'settings',
        'settings': {
            'app_name': 'EyeDetect',
            'admin_email': 'admin@example.com',
            'system_mode': 'Online',
            'email_notifications': True,
            'two_factor_auth': False,
            'maintenance_mode': False,
        },
    })
    return render(request, 'admin_settings.html', context)


def admin_activity(request):
    context = _get_admin_data()
    context.update({'page_title': 'Riwayat Aktivitas', 'current_page': 'activity'})
    return render(request, 'admin_activity.html', context)


def admin_users(request):

    users = User.objects.all()

    print("TOTAL USER:", users.count())

    return render(
        request,
        'admin_users.html',
        {
            'users': users,
            'total_users': users.count()
        }
    )

def admin_settings(request):
    context = _get_admin_data()
    context.update({'page_title': 'Pengaturan', 'current_page': 'settings'})
    return render(request, 'admin_settings.html', context)
