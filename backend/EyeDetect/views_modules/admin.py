from EyeDetect import views as core_views


def admin_dashboard(request):
    return core_views.admin_dashboard(request)


def admin_dataset(request):
    return core_views.admin_dataset(request)


def admin_dataset_detail(request, split, class_slug):
    return core_views.admin_dataset_detail(request, split, class_slug)


def admin_dataset_image(request, split, class_slug, filename):
    return core_views.admin_dataset_image(request, split, class_slug, filename)


def admin_predictions(request):
    return core_views.admin_predictions(request)


def admin_model_cnn(request):
    return core_views.admin_model_cnn(request)


def admin_users(request):
    return core_views.admin_users(request)


def admin_settings(request):
    return core_views.admin_settings(request)


def admin_activity(request):
    return core_views.admin_activity(request)
