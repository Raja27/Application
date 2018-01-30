from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.utils import timezone
from . import models
from . import serializers
import logging

logger = logging.getLogger('django.request')


class ApplicationCreate(APIView):

    # permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'application/application.html'

    def post(self, request):
        response = dict()
        code = status.HTTP_400_BAD_REQUEST
        status_message = "Failed"
        data = request.data.copy()
        app_no = None
        try:
            serializer = serializers.ApplicationsSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response.update(serializer.data)
                app_no = serializer.data.get('app_ref_no')
            code = status.HTTP_201_CREATED
            status_message = "Success"
        except Exception as e:
            logger.error(repr(e))
        response.update({'status_message': status_message})
        return redirect('/#{}'.format(app_no), {'app_no': app_no})
        
        
class ApplicationEdit(APIView):

    permission_classes = (IsAdminUser,)

    def put(self, request, pk):
        response = dict()
        code = status.HTTP_400_BAD_REQUEST
        status_message = "Failed"
        data = request.data.copy()
        try:
            if models.Applications.objects.filter(id=pk).exists():
                application = models.Applications.objects.get(id=pk)
                data.update(
                    {
                        'status_changed_at': timezone.now(),
                        'status_changed_by': request.user.email,
                        'updated_by': request.user.email
                    }
                )
                serializer = serializers.ApplicationsEditSerializers(application, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    response.update(serializers.ApplicationsDetailSerializers(application).data)
                code = status.HTTP_200_OK
                status_message = "Successfully"
        except Exception as e:
            logger.error(repr(e))
        response.update({'status_message': status_message})
        return Response(response, code)


class ApplicationDetail(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        response = dict()
        code = status.HTTP_400_BAD_REQUEST
        status_message = "Failed"
        try:
            if models.Applications.objects.filter(id=pk).exists():
                application = models.Applications.objects.get(id=pk)
                serializer = serializers.ApplicationsDetailSerializers(application).data
                response.update(serializer)
                code = status.HTTP_200_OK
                status_message = "Success"
        except Exception as e:
            logger.error(repr(e))
        response.update({'status_message': status_message})
        return Response(response, code)


class ApplicationList(ListAPIView):

    queryset = models.Applications.objects.all().order_by('status')
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ApplicationsListSerializers
    pagination_class = serializers.LimitTenPagination

    def get_queryset(self):
        if self.request.GET.get('status'):
            return self.queryset.filter(status=self.request.GET.get('status'))
        else:
            return sorted(self.queryset.all(), key=lambda m: m.cust_order_by())
