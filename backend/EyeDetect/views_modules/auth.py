from EyeDetect import views as core_views


def welcome(request):
    return core_views.welcome(request)


def show_login(request):
    return core_views.show_login(request)


def show_admin_login(request):
    return core_views.show_admin_login(request)


def login_proses(request):
    return core_views.login_proses(request)


def show_daftar(request):
    return core_views.show_daftar(request)


def daftar_proses(request):
    return core_views.daftar_proses(request)


def password_baru(request):
    return core_views.password_baru(request)


def logout_user(request):
    return core_views.logout_user(request)
