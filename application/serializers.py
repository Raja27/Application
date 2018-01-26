from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers, pagination

from . import models


FIELDS_EXCLUDE = ('created_on', 'updated_on', 'created_by', 'updated_by')


class LimitTenPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'


class ApplicationsSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Applications
        exclude = FIELDS_EXCLUDE


class ApplicationsDetailSerializers(serializers.ModelSerializer):
    status_changed_at = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Applications
        exclude = FIELDS_EXCLUDE

    def get_status_changed_at(self, obj):
        if obj.status_changed_at:
            return naturaltime(obj.status_changed_at)
        return obj.status_changed_at

    def get_file_name(self, obj):
        if obj.resume:
            return obj.resume.name
        return ''


class ApplicationsEditSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Applications
        fields = ('status', 'status_changed_by', 'status_changed_at', 'updated_by')


class ApplicationsListSerializers(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()
    status_changed_at = serializers.SerializerMethodField()

    class Meta:
        model = models.Applications
        fields = ('id', 'app_ref_no', 'name', 'status', 'created_on', 'status_changed_at')

    def get_created_on(self, obj):
        return naturaltime(obj.created_on)

    def get_status_changed_at(self, obj):
        if obj.status_changed_at:
            return naturaltime(obj.status_changed_at)
        return obj.status_changed_at

