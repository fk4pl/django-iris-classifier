import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User

try:
    u = User.objects.get(username='admin')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print('✓ Admin superuser ve staff yapıldı')
except User.DoesNotExist:
    print('✗ Admin kullanıcısı bulunamadı')
