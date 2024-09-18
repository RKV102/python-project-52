from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import User
from .forms import UserForm


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
        form = UserForm()
        return render(
            request,
            'users/create.html',
            context={'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        return render(
            request,
            'users/create.html',
            {'form': form}
        )


class UpdateUserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        form = UserForm(instance=user)
        return render(
            request,
            'users/update.html',
            context={'form': form, 'user_id': user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        return render(
            request,
            'users/create.html',
            {'form': form}
        )


class DeleteUserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        return render(
            request,
            'users/delete.html',
            context={'user': user}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('users')
