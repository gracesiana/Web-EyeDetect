import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EyeDetect.settings')
import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from EyeDetect.views import dashboard, admin_dashboard

User = get_user_model()
user = User.objects.filter(email='admin@eyedetect.com').first()
rf = RequestFactory()

for view_name, view_func in [('dashboard', dashboard), ('admin_dashboard', admin_dashboard)]:
    req = rf.get('/' if view_name == 'dashboard' else '/admin-panel/')
    req.user = user
    req.session = {}
    SessionMiddleware(lambda req: None).process_request(req)
    req.session.save()
    setattr(req, '_messages', FallbackStorage(req))
    MessageMiddleware(lambda req: None).process_request(req)
    print('---', view_name, '---')
    try:
        response = view_func(req)
        print('status', response.status_code)
        print(response.content[:1000].decode('utf-8', 'ignore'))
    except Exception as e:
        import traceback
        traceback.print_exc()
