from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm, UserChangeForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users/index.html',
            context={'users': users}
        )


class CreateUserView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users')
    success_message = 'Регистрация прошла успешно'


class UpdateUserView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = 'Данные пользователя были обновлены'


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь был удалён'
