from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def welcome(request):
    return render(request, 'welcome.html')


def show_login(request):
    return render(request, 'login.html')


def login_proses(request):
    if request.method != 'POST':
        return redirect('login')

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    if not email or not password:
        messages.error(request, 'Email dan password harus diisi.')
        return render(request, 'login.html')

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
        login(request, user)
        return redirect('dashboard')

    messages.error(request, 'Email atau password tidak valid.')
    return render(request, 'login.html')


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
    if request.method == 'POST':
        logout(request)
    return redirect('login')


def dashboard(request):
    screening_count = 0
    return render(request, 'dashboard.html', {
        'screeningCount': screening_count,
    })

def deteksi(request):
    return render(request, 'deteksi.html')

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