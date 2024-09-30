from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import (LoginView as DjangoLoginView,
                                       LogoutView as DjangoLogoutView)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.contrib import messages


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginView(SuccessMessageMixin, DjangoLoginView):
    success_message = _('Welcome, %(username)s!')
    template_name = 'registration/login.html'


class LogoutView(DjangoLogoutView):

    def get_success_url(self):
        success_url = super(LogoutView, self).get_success_url()
        messages.add_message(
            self.request, messages.SUCCESS,
            _('We will be glad to see you again')
        )
        return success_url
