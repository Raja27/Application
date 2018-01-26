from django.conf.urls import url
from django.views.generic import TemplateView
from . import api


urlpatterns = [
    url(r'^api/application/create', api.ApplicationCreate.as_view()),
    url(r'^api/application/edit/(?P<pk>[0-9]+)/', api.ApplicationEdit.as_view()),
    url(r'^api/application/list/', api.ApplicationList.as_view()),
    url(r'^api/application/detail/(?P<pk>[0-9]+)/', api.ApplicationDetail.as_view()),

    url(r'^applications/$', TemplateView.as_view(template_name='application/application_list.html')),
    url(r'^applications/detail/', TemplateView.as_view(template_name='application/application_detail.html')),
    url(r'^$', TemplateView.as_view(template_name='application/application.html')),
]
