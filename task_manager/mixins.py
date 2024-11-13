from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import AccessMixin
from task_manager.users.models import User
from django.contrib.auth.mixins import (LoginRequiredMixin as
                                        DjangoLoginRequiredMixin)


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please log in'),
                extra_tags='danger'
            )
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class BaseSuccessUrlMixin:
    redirect_url = '/'

    def get_success_url(self):
        return reverse_lazy(self.redirect_url)


class UsageCheckMixin(AccessMixin):
    message = ''
    model = User
    redirect_url = 'index'
    methods = ('POST',)

    def dispatch(self, request, *args, **kwargs):
        model_item_id = kwargs['pk']
        model_item = get_object_or_404(self.model, id=model_item_id)
        if request.method not in self.methods:
            return super().dispatch(request, *args, **kwargs)
        if self.model is User and model_item.task_executor.exists():
            messages.error(request, self.message, extra_tags='danger')
            return redirect(self.redirect_url)
        if model_item.task_set.exists():
            messages.error(request, self.message, extra_tags='danger')
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
