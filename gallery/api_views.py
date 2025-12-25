from rest_framework import viewsets
from .models import IrisSample
from .api_serializers import IrisSampleSerializer


class IrisSampleViewSet(viewsets.ModelViewSet):
    queryset = IrisSample.objects.all()
    serializer_class = IrisSampleSerializer
