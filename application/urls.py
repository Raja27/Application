from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^create', api.ApplicationCreate.as_view()),
    url(r'^list', api.ApplicationList.as_view()),
]