from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions import mixins
from flurryapp.models import DataDriver
from flurryapp.serializers.data_driver_serializer import DataDriverSerializer

COLUMNS_TO_CONVERT = ['rpm', 'throttle', 'accelerator', 'rpm', 'speed']


class DataDriverViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for DataDriver 
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """
    queryset = DataDriver.objects.all()
    serializer_class = DataDriverSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        ride = request.query_params.get('ride', None)
        data_unit = request.query_params.get('data_unit', None)
        if ride is not None and len(obj) > 0:
            data = obj[int(ride)][int(data_unit)] if data_unit is not None else obj[int(ride)]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return super(DataDriverViewSet, self).retrieve(request, *args, **kwargs)

    @detail_route(methods=['GET'])
    def merged(self, request, *args, **kwargs):
        driving_data = self.get_object()
        if len(driving_data) is not 0:
            data = reduce(lambda x, y: x + y, driving_data.data)
            # data = [self.__convert_data_unit_values_to_numeric_values(data_unit) for ride in driving_data.data for data_unit in ride]
        else:
            data = driving_data.data

        return Response(data, status=status.HTTP_200_OK)

    def __convert_data_unit_values_to_numeric_values(self, data_unit):
        new_data = dict()
        for key, value in data_unit.iteritems():
            if key in COLUMNS_TO_CONVERT:
                new_data[key] = float(value)
            else:
                new_data[key] = value

        return new_data
