from django.conf.urls import url
from django.views.generic import TemplateView
from . import api

urlpatterns = [
    url(r'^login/$', TemplateView.as_view(template_name='application/login.html'), name='login'),
    url(r'^api/login/$', api.Login.as_view()),
    url(r'^api/logout/$', api.Logout.as_view()),
]