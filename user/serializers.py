from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers, pagination

from . import models


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
