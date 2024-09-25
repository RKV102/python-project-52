from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginView(SuccessMessageMixin, DjangoLoginView):
    success_message = 'Добро пожаловать, %(username)s'
    template_name = 'registration/login.html'
