from rest_framework import serializers
from django.contrib.auth.models import User
from flurryapp.models import Driver


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'name')

    def create(self, validated_data):
        validated_data.pop('name')  # name is not a property of user model
        return super(UserSerializer, self).create(validated_data)
