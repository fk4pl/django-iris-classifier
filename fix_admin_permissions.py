import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from gallery.models import IrisSample, Collection

# Admin kullanıcısını al
admin_user = User.objects.get(username='admin')

# IrisSample ve Collection için tüm permissions'ları al
iris_ct = ContentType.objects.get_for_model(IrisSample)
collection_ct = ContentType.objects.get_for_model(Collection)

iris_permissions = Permission.objects.filter(content_type=iris_ct)
collection_permissions = Permission.objects.filter(content_type=collection_ct)

# Admin'e tüm permissions ver
admin_user.user_permissions.add(*iris_permissions)
admin_user.user_permissions.add(*collection_permissions)

print(f'✓ Admin\'e {len(iris_permissions) + len(collection_permissions)} permission verildi')

# Şifreyi güvenli hale getir
admin_user.set_password('AdminSecure2025!')
admin_user.save()

print('✓ Admin şifresi güvenli hale getirildi: AdminSecure2025!')
print('Yeni admin şifresi: AdminSecure2025!')
