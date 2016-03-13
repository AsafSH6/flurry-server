from rest_framework import serializers
from flurryapp.models import Driver


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(many=True, view_name='profiles-detail', read_only=True)
    driving_data = serializers.HyperlinkedIdentityField(view_name='data-drivers-detail', read_only=True)

    class Meta:
        model = Driver
        fields = ('id', 'name', 'creation_date', 'driving_data', 'profiles')
