from EyeDetect import views as core_views


def dashboard(request):
    return core_views.dashboard(request)


def deteksi(request):
    return core_views.deteksi(request)


def cara_kerja(request):
    return core_views.cara_kerja(request)


def profile(request):
    return core_views.profile(request)


def riwayat(request):
    return core_views.riwayat(request)


def faq(request):
    return core_views.faq(request)
