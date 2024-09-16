from django.shortcuts import render, HttpResponse
from django.views import View
from .models import User
from .forms import CreateUserForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users/index.html',
            context={'users': users}
        )


class CreateUserView(View):
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(
            request,
            'users/create.html',
            context={'form': form}
        )

    def post(self, request, *args, **kwargs):
        return HttpResponse('Success')
