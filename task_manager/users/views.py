from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _
from task_manager.mixins import LoginRequiredMixin


USERS_URL = reverse_lazy('users')


class PermissionRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        current_user_id = request.session.get('_auth_user_id')
        target_user_id = str(kwargs['pk'])
        if current_user_id != target_user_id:
            messages.error(
                request,
                _("You don't have the rights to change another user"),
                extra_tags='danger'
            )
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UsageCheckMixin(AccessMixin):
    message_text = _("User can't be deleted because he's used in the task")

    def dispatch(self, request, *args, **kwargs):
        model_item_id = kwargs['pk']
        model_item = get_object_or_404(self.model, id=model_item_id)
        if model_item.task_performer.all():
            messages.error(
                request,
                self.message_text,
                extra_tags='danger'
            )
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


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


class UpdateUserView(LoginRequiredMixin, PermissionRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    login_url = USERS_URL
    redirect_field_name = None
    model = User
    form_class = UserChangeForm
    template_name = 'users/update.html'
    success_url = USERS_URL
    success_message = _('User has been updated')


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin,
                     UsageCheckMixin, SuccessMessageMixin,
                     DeleteView):
    login_url = USERS_URL
    redirect_field_name = None
    model = User
    template_name = 'users/delete.html'
    success_url = USERS_URL
    success_message = _('User has been deleted')
