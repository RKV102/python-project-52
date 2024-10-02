from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from urllib.parse import urlsplit
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.utils.translation import gettext as _


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
