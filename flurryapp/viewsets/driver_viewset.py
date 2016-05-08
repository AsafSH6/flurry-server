from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions import mixins
from flurryapp.models import Driver
from flurryapp.serializers.driver_serializer import DriverSerializer
import json


class DriverViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for DataDriver 
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    @detail_route(methods=['POST'])
    def insert_driving_data(self, request, *args, **kwargs):
        driving_data_json = request.data
        if isinstance(driving_data_json, unicode):
            driving_data_json = json.loads(driving_data_json)
        if isinstance(driving_data_json, (dict, list)):
            # print driving_data_json
            driver_id = self.kwargs['pk']
            Driver.objects.append_new_driving_data(driver_id=driver_id, driving_data=driving_data_json)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

