from rest_framework import viewsets
from rest_framework_extensions import mixins
from flurryapp.models import DataDriver
from flurryapp.serializers.data_driver_serializer import DataDriverSerializer


class DataDriverViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    queryset = DataDriver.objects.all()
    serializer_class = DataDriverSerializer
