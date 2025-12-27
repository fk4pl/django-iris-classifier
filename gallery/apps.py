from django.apps import AppConfig


class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gallery'

    def ready(self):
        """Admin hesabını otomatik oluştur"""
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        User = get_user_model()
        
        # Admin hesabını kontrol et ve oluştur
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print("✓ Admin hesabı oluşturuldu (admin/admin)")
        
        # Writer grubunu oluştur
        writer_group, created = Group.objects.get_or_create(name='writer')
        if created:
            print("✓ Writer grubu oluşturuldu")
