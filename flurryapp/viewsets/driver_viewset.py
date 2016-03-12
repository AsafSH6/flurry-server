from rest_framework import viewsets
from rest_framework_extensions import mixins
from flurryapp.models import Driver
from flurryapp.serializers.driver_serializer import DriverSerializer


class DriverViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
