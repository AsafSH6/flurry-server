from rest_framework import serializers
from flurryapp.models import Profile
from flurryapp.serializers.driver_serializer import DriverSerializer


class ProfileSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(instance='driver', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'avg_rpm', 'driver')