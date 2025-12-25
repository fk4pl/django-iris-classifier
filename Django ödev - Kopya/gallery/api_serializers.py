from rest_framework import serializers
from .models import IrisSample


class IrisSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrisSample
        fields = ['id', 'instance_id', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
