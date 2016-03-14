from rest_framework import viewsets
from rest_framework_extensions import mixins
from flurryapp.models import Profile
from flurryapp.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for DataDriver 
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
    post/get requests.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
