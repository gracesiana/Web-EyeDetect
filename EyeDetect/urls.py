from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # AUTH
    path('', views.welcome, name='home'),
    path('login/', views.show_login, name='login'),
    path('login/admin/', views.show_admin_login, name='admin_login'),
    path('login/proses/', views.login_proses, name='login_proses'),
    path('logout/', views.logout_user, name='logout'),

    # REGISTER
    path('daftar/', views.show_daftar, name='register'),
    path('daftar/proses/', views.daftar_proses, name='register_proses'),

    # PASSWORD
    path('lupa-password/', views.lupa_password, name='lupa_password'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    # ADMIN PANEL (custom admin dashboard)
    path('admin-panel/', views.admin_dashboard, name='admin_panel'),
    path('admin-panel/dataset/', views.admin_dataset, name='admin_panel_dataset'),
    path('admin-panel/prediksi/', views.admin_predictions, name='admin_panel_predictions'),
    path('admin-panel/model-cnn/', views.admin_model_cnn, name='admin_panel_model'),
    path('admin-panel/aktivitas/', views.admin_activity, name='admin_panel_activity'),
    path('admin-panel/pengguna/', views.admin_users, name='admin_panel_users'),
    path('admin-panel/pengaturan/', views.admin_settings, name='admin_panel_settings'),

    # FITUR UTAMA
    path('deteksi/', views.deteksi, name='deteksi'),
    path('cara-kerja/', views.cara_kerja, name='cara_kerja'),
    path('profile/', views.profile, name='profile'),
    path('riwayat-skrining/', views.riwayat, name='riwayat_skrining'),
    path('pengaturan/', views.pengaturan, name='pengaturan'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)