from django.shortcuts import render

def welcome(request):
    return render(request, 'welcome.html')

def show_login(request):
    return render(request, 'login.html')

def login_proses(request):
    # Add login processing logic here
    pass

def show_daftar(request):
    return render(request, 'daftar.html')

def daftar_proses(request):
    # Add registration processing logic here
    pass

def lupa_password(request):
    # Add logic for password recovery here
    return render(request, 'lupa-password.html')

def logout_user(request):
    # Add logic for user logout here
    pass

def dashboard(request):
    return render(request, 'dashboard.html')

def deteksi(request):
    return render(request, 'deteksi.html')

def cara_kerja(request):
    return render(request, 'cara-kerja.html')

def profile(request):
    return render(request, 'profile.html')

def riwayat(request):
    return render(request, 'riwayat-skrining.html')

def pengaturan(request):
    return render(request, 'pengaturan.html')