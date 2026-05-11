from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # AUTH
    path('', views.welcome, name='home'),
    path('login/', views.show_login, name='login'),
    path('login/proses/', views.login_proses, name='login_proses'),
    path('logout/', views.logout_user, name='logout'),

    # REGISTER
    path('daftar/', views.show_daftar, name='register'),
    path('daftar/proses/', views.daftar_proses, name='register_proses'),

    # PASSWORD
    path('lupa-password/', views.lupa_password, name='lupa_password'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # FITUR UTAMA
    path('deteksi/', views.deteksi, name='deteksi'),
    path('cara-kerja/', views.cara_kerja, name='cara_kerja'),
    path('profile/', views.profile, name='profile'),
    path('riwayat-skrining/', views.riwayat, name='riwayat_skrining'),
    path('pengaturan/', views.pengaturan, name='pengaturan'),
]