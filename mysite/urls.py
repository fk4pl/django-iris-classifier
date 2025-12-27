from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from gallery.api_views import IrisSampleViewSet

router = routers.DefaultRouter()
router.register(r'api/iris', IrisSampleViewSet, basename='api-iris')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),
    path('', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
