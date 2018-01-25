from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers, pagination

from . import models


FIELDS_EXCLUDE = ('created_on', 'updated_on', 'created_by', 'updated_by')


class LimitTenPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'


class ApplicationsSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Applications
        exclude = FIELDS_EXCLUDE


class ApplicationsListSerializers(serializers.ModelSerializer):
    created_no = serializers.SerializerMethodField()

    class Meta:
        model = models.Applications
        fields = ('id', 'app_ref_no', 'name', 'status', 'created_no')

    def get_created_on(self, obj):
        return naturaltime(obj.created_on)
