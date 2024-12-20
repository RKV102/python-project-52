from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.users.models import User
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (LoginRequiredMixin, SuccessUrlMixin,
                                 DeletionProtectedMixin as
                                 BaseDeletionProtectedMixin,
                                 ContextDataMixin)


class RedirectUrlMixin:
    redirect_url = 'users'


class DeletionProtectedMixin(BaseDeletionProtectedMixin):
    message = _("User can't be deleted because he's used in the task")
    methods = ('GET', 'POSTS')


class ModelMixin:
    model = User


class PermissionRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        target_user_id = kwargs['pk']
        if request.user.id != target_user_id:
            messages.error(
                request,
                _("You don't have the rights to change another user"),
                extra_tags='danger'
            )
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class IndexView(ModelMixin, ListView):
    template_name = 'users/index.html'
    context_object_name = 'users'


class CreateUserView(ModelMixin, ContextDataMixin, RedirectUrlMixin,
                     SuccessUrlMixin, SuccessMessageMixin, CreateView):
    template_label_name = _('Creating user')
    url_name = 'users_create'
    form_class = UserCreationForm
    template_name = 'general/create.html'
    success_message = _('Registration was successful')
    redirect_url = 'login'


class UpdateUserView(ModelMixin, ContextDataMixin, RedirectUrlMixin,
                     SuccessUrlMixin, LoginRequiredMixin,
                     PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    template_label_name = _('Editing user')
    url_name = 'users_update'
    form_class = UserChangeForm
    template_name = 'general/update.html'
    success_message = _('User has been updated')


class DeleteUserView(ModelMixin, ContextDataMixin, RedirectUrlMixin,
                     SuccessUrlMixin, LoginRequiredMixin,
                     PermissionRequiredMixin, DeletionProtectedMixin,
                     SuccessMessageMixin, DeleteView):
    template_label_name = _('Deleting user')
    url_name = 'users_delete'
    template_name = 'general/delete.html'
    success_message = _('User has been deleted')
