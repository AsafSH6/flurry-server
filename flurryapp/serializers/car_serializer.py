from rest_framework import serializers
from flurryapp.models import Car
from flurryapp.serializers.driver_serializer import DriverSerializer


class CarSerializer(serializers.ModelSerializer):
    owner = DriverSerializer(instance='driver')
    
    """
    CarSerializer - serializer for car model
    owner's instance is driver
    """

    class Meta:
        model = Car
        fields = ('id', 'manufacturer', 'production_year', 'model', 'owner')
