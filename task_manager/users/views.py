from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.users.models import User
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixin, BaseSuccessUrlMixin
from task_manager.decorators import rollbar_decorator
from django.utils.decorators import method_decorator


class SuccessUrlMixin(BaseSuccessUrlMixin):
    redirect_url = 'users'


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


class UsageCheckMixin(AccessMixin):
    message_text = _("User can't be deleted because he's used in the task")

    def dispatch(self, request, *args, **kwargs):
        model_item_id = kwargs['pk']
        model_item = get_object_or_404(self.model, id=model_item_id)
        if model_item.task_executor.all():
            messages.error(
                request,
                self.message_text,
                extra_tags='danger'
            )
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class IndexView(ModelMixin, ListView):
    template_name = 'users/index.html'
    context_object_name = 'users'


@method_decorator(rollbar_decorator, name='post')
class CreateUserView(ModelMixin, SuccessUrlMixin,
                     SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'users/create.html'
    success_message = _('Registration was successful')
    redirect_url = 'login'


@method_decorator(rollbar_decorator, name='post')
class UpdateUserView(ModelMixin, SuccessUrlMixin,
                     LoginRequiredMixin, PermissionRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'users/update.html'
    success_message = _('User has been updated')


@method_decorator(rollbar_decorator, name='post')
class DeleteUserView(ModelMixin, SuccessUrlMixin, LoginRequiredMixin,
                     PermissionRequiredMixin, UsageCheckMixin,
                     SuccessMessageMixin, DeleteView):
    template_name = 'users/delete.html'
    success_message = _('User has been deleted')
