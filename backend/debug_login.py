import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EyeDetect.settings')
import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from EyeDetect.views import login_proses

User = get_user_model()
user = User.objects.filter(email='admin@eyedetect.com').first()

rf = RequestFactory()
req = rf.post('/login/proses/', {'email': 'admin@eyedetect.com', 'password': 'admin123', 'login_as_admin': '1'})
req.user = user

SessionMiddleware(lambda req: None).process_request(req)
req.session.save()
setattr(req, '_messages', FallbackStorage(req))
MessageMiddleware(lambda req: None).process_request(req)

try:
    resp = login_proses(req)
    print('STATUS', getattr(resp, 'status_code', None))
    print('URL', getattr(resp, 'url', None))
    print('CONTENT', getattr(resp, 'content', b'')[:1000])
except Exception as e:
    import traceback
    traceback.print_exc()
