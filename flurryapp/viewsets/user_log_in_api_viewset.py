from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserLogInAPIViewSet(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous():
            data = {
                'user_id': request.user.pk,
                'driver_id': request.user.drivers.first().pk
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response('Missing credentials', status=status.HTTP_401_UNAUTHORIZED)
