from rest_framework import viewsets
from rest_framework_extensions import mixins
from flurryapp.models import Profile
from flurryapp.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
