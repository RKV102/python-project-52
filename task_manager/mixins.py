from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _


class BaseAuthMixin(AccessMixin):
    redirect_field_name = None


class LoginRequiredMixin(BaseAuthMixin):
    login_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please log in'),
                extra_tags='danger'
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(BaseAuthMixin):
    login_url = reverse_lazy('tasks')

    def dispatch(self, request, *args, **kwargs):
        current_user_id = request.session.get('_auth_user_id')
        current_task_id = kwargs['pk']
        target_user_id = str(
            get_object_or_404(
                Task,
                id=current_task_id
            ).creator.id
        )
        if current_user_id != target_user_id:
            messages.error(
                request,
                _("You don't have the rights to change another user"),
                extra_tags='danger'
            )
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)
