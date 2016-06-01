from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions import mixins
from flurryapp.models import DataDriver
from flurryapp.serializers.data_driver_serializer import DataDriverSerializer


class DataDriverViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for DataDriver 
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """
    queryset = DataDriver.objects.all()
    serializer_class = DataDriverSerializer

    @detail_route(methods=['GET'])
    def merged(self, request, *args, **kwargs):
        driving_data = self.get_object()
        data = reduce(lambda x, y: x + y, driving_data.data)
        return Response(data, status=status.HTTP_200_OK)
