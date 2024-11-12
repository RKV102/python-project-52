from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib.auth.mixins import (LoginRequiredMixin as
                                        DjangoLoginRequiredMixin)


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self, request):
        messages.error(
            request,
            _('You are not logged in! Please log in'),
            extra_tags='danger'
        )
        return redirect(self.login_url)


class BaseSuccessUrlMixin:
    redirect_url = '/'

    def get_success_url(self):
        return reverse_lazy(self.redirect_url)
