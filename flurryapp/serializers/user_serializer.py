from rest_framework import serializers
from django.contrib.auth.models import User
from flurryapp.models import Driver


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'drivers')
