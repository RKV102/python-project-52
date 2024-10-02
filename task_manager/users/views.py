from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from urllib.parse import urlsplit
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages


USERS_URL = reverse_lazy('users')


class LoginRequiredMixin(AccessMixin):

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        login_scheme, login_netloc = urlsplit(resolved_login_url)[:2]
        current_scheme, current_netloc = urlsplit(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
                not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )

    def dispatch(self, request, *args, **kwargs):
        current_user_id = request.session.get('_auth_user_id')
        target_used_id = str(kwargs['pk'])
        if (not request.user.is_authenticated
                or current_user_id != target_used_id):
            messages.error(
                request,
                _("You don't have the rights to change another user"),
                extra_tags='danger'
            )
            return self.handle_no_permission()
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
