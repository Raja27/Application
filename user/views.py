from django.views.generic import FormView, RedirectView
from django.contrib.auth import logout


class LogoutView(RedirectView):

    url = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)