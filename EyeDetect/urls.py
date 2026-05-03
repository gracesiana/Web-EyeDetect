from django.contrib import admin
from django.urls import path
from . import views   # pastikan ini satu folder dengan views.py

urlpatterns = [

    # =========================
    # ADMIN
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # HALAMAN UTAMA
    # =========================
    path('', views.welcome, name='welcome'),

    # =========================
    # AUTH USER
    # =========================

    # Login
    path('login/', views.show_login, name='login'),
    path('login/proses/', views.login_proses, name='login_proses'),

    # Daftar
    path('daftar/', views.show_daftar, name='daftar'),
    path('daftar/proses/', views.daftar_proses, name='daftar_proses'),

    # Lupa Password
    path('lupa-password/', views.lupa_password, name='lupa_password'),

    # Logout
    path('logout/', views.logout_user, name='logout'),

    # =========================
    # DASHBOARD USER
    # =========================

    path('dashboard/', views.dashboard, name='dashboard'),

    path('deteksi/', views.deteksi, name='deteksi'),
    path('cara-kerja/', views.cara_kerja, name='cara_kerja'),
    path('profile/', views.profile, name='profile'),
    path('riwayat-skrining/', views.riwayat, name='riwayat_skrining'),
    path('pengaturan/', views.pengaturan, name='pengaturan'),
]