from rest_framework import viewsets
from rest_framework_extensions import mixins
from flurryapp.models import Car
from flurryapp.serializers.car_serializer import CarSerializer


class CarViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
