from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _
from ..mixins.views import LoginRequiredMixin


USERS_URL = reverse_lazy('users')


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users/index.html',
            context={'users': users}
        )


class CreateUserView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/create.html'
    success_url = USERS_URL
    success_message = _('Registration was successful')


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = USERS_URL
    redirect_field_name = None
    model = User
    form_class = UserChangeForm
    template_name = 'users/update.html'
    success_url = USERS_URL
    success_message = _('User has been updated')


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = USERS_URL
    redirect_field_name = None
    model = User
    template_name = 'users/delete.html'
    success_url = USERS_URL
    success_message = _('User has been deleted')
