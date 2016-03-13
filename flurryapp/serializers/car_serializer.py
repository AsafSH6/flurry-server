from rest_framework import serializers
from flurryapp.models import Car
from flurryapp.serializers.driver_serializer import DriverSerializer


class CarSerializer(serializers.ModelSerializer):
    owner = DriverSerializer(instance='driver')

    class Meta:
        model = Car
        fields = ('id', 'manufacturer', 'production_year', 'model', 'owner')
