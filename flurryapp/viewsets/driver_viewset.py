from rest_framework import viewsets
from rest_framework_extensions import mixins
from flurryapp.models import Driver
from flurryapp.serializers.driver_serializer import DriverSerializer


class DriverViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for DataDriver 
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
