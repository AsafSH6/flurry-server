from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_extensions import mixins
from django.contrib.auth.models import User
from flurryapp.serializers.user_serializer import UserSerializer
from flurryapp.models import Driver


class UserViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for User
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            driver_name = request.data['name'][0]

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                driver = Driver(name=driver_name, user=user).save()
                return Response(driver.pk, status=status.HTTP_201_CREATED)
            else:
                return Response('User already exists', status=status.HTTP_400_BAD_REQUEST)
        except KeyError, IndexError:
            return Response('driver name is missing', status=status.HTTP_400_BAD_REQUEST)
