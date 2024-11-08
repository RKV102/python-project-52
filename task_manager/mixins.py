from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.utils.translation import gettext as _


class LoginRequiredMixin(AccessMixin):
    redirect_field_name = None
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please log in'),
                extra_tags='danger'
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BaseSuccessUrlMixin:
    redirect_url = '/'

    def get_success_url(self):
        return reverse_lazy(self.redirect_url)
