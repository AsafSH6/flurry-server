from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from flurryapp.models import Driver


class FeatureExtractAPIViewSet(APIView):

    def get(self, request, *args, **kwargs):
        extracted_features = Driver.objects.extract_features()
        return Response(extracted_features, status=status.HTTP_200_OK)