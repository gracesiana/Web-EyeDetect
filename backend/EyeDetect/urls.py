from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views_modules import auth as auth_views
from .views_modules import admin as admin_views
from .views_modules import user as user_views
from . import views

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # AUTH
    path('', auth_views.welcome, name='home'),
    path('login/', auth_views.show_login, name='login'),
    path('login/admin/', auth_views.show_admin_login, name='admin_login'),
    path('login/proses/', auth_views.login_proses, name='login_proses'),
    path('logout/', auth_views.logout_user, name='logout'),

    # REGISTER
    path('daftar/', auth_views.show_daftar, name='register'),
    path('daftar/proses/', auth_views.daftar_proses, name='register_proses'),

    # PASSWORD
    path('password-baru/', auth_views.password_baru, name='password_baru'),

    # DASHBOARD
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('frontend/dashboard/', user_views.dashboard, name='frontend_dashboard'),
    # ADMIN PANEL (custom admin dashboard)
    path('admin-panel/', admin_views.admin_dashboard, name='admin_panel'),
    path('admin-panel/dataset/', admin_views.admin_dataset, name='admin_panel_dataset'),
    path(
        'admin-panel/dataset/<str:split>/<str:class_slug>/',
        admin_views.admin_dataset_detail,
        name='admin_panel_dataset_detail',
    ),
    path(
        'admin-panel/dataset-image/<str:split>/<str:class_slug>/<path:filename>/',
        admin_views.admin_dataset_image,
        name='admin_panel_dataset_image',
    ),
    path('admin-panel/prediksi/', admin_views.admin_predictions, name='admin_panel_predictions'),
    path('admin-panel/model-cnn/', admin_views.admin_model_cnn, name='admin_panel_model'),
    path('admin-panel/aktivitas/', admin_views.admin_activity, name='admin_panel_activity'),
    path('admin-panel/pengguna/', admin_views.admin_users, name='admin_panel_users'),
    path('admin-panel/pengaturan/', admin_views.admin_settings, name='admin_panel_settings'),

    # FITUR UTAMA
    path('deteksi/', user_views.deteksi, name='deteksi'),
    path('cara-kerja/', user_views.cara_kerja, name='cara_kerja'),
    path('profile/', user_views.profile, name='profile'),
    path('riwayat-skrining/', user_views.riwayat, name='riwayat_skrining'),
    path('faq/', user_views.faq, name='faq'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
