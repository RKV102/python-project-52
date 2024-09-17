from django.shortcuts import render, redirect
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
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        return render(
            request,
            'users/create.html',
            {'form': form}
        )
