from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect


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


class BaseUsageCheckMixin(AccessMixin):
    message_text = ''
    redirect_url = ''

    def dispatch(self, request, *args, **kwargs):
        model_item_id = kwargs['pk']
        model_item = get_object_or_404(self.model, id=model_item_id)
        if model_item.task_set.all():
            messages.error(
                request,
                self.message_text,
                extra_tags='danger'
            )
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class BaseSuccessUrlMixin:
    redirect_url = ''

    def get_success_url(self):
        return reverse_lazy(self.redirect_url)
