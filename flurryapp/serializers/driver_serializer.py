from rest_framework import serializers
from flurryapp.models import Driver


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(many=True, view_name='profiles-detail', read_only=True)
    cars = serializers.HyperlinkedRelatedField(many=True, view_name='cars-detail', read_only=True)
    driving_data = serializers.HyperlinkedIdentityField(view_name='data-drivers-detail')

    """
    profiles - Hyperlinked relationship between DriverModel and Profiles model(
            driver serves as "foreign key" in the profile model)
    driver_data - Hyperlinked relationship between DrivingData and Driver (driver
            serves as the identity fields in the data_driver model)
    """
    class Meta:
        model = Driver
        fields = ('id', 'name', 'creation_date', 'driving_data', 'profiles', 'cars')
