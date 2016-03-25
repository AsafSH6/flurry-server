from rest_framework import serializers
from flurryapp.models import DataDriver


class DataDriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataDriver

