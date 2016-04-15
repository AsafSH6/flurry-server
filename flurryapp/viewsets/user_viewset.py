from rest_framework import viewsets
from rest_framework_extensions import mixins
from django.contrib.auth.models import User
from flurryapp.serializers.user_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for User
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
