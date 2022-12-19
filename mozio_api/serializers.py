from rest_framework import serializers
from mozio_api.models import ProviderModel
from mozio_api.models import ServiceAreaModel


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderModel
        fields = '__all__'

class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAreaModel
        fields = '__all__'