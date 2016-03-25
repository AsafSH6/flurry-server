from rest_framework import serializers
from flurryapp.models import Car, Driver
from flurryapp.serializers.driver_serializer import DriverSerializer


class CarSerializer(serializers.ModelSerializer):
    """
    CarSerializer - serializer for car model
    owner's instance is driver
    """
    owner_details = DriverSerializer(read_only=True, source='owner')  # display the details of the owner
    owner = serializers.PrimaryKeyRelatedField(queryset=Driver.objects, write_only=True)  # allow to add owner by id

    class Meta:
        model = Car
        fields = ('id', 'manufacturer', 'production_year', 'model', 'owner_details', 'owner')
