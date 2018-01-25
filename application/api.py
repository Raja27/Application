from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from . import models
from . import serializers
import logging

logger = logging.getLogger('django.request')


class ApplicationCreate(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        response = dict()
        code = status.HTTP_400_BAD_REQUEST
        status_message = "Failed"
        data = request.data.copy()
        try:
            serializer = serializers.ApplicationsSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response.update(serializer.data)
            code = status.HTTP_201_CREATED
            status_message = "Success"
        except Exception as e:
            logger.error(repr(e))
        response.update({'status_message': status_message})
        return Response(response, code)


class ApplicationList(ListAPIView):

    queryset = models.Applications.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ApplicationsSerializers
    pagination_class = serializers.LimitTenPagination

    def get_queryset(self):
        if self.request.GET.get('status') :
            return self.queryset.filter(status=self.request.GET.get('status'))
        else:
            return self.queryset.all()
