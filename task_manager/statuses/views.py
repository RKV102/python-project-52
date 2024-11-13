from django.views.generic import ListView
from .models import Status
from .forms import StatusForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (LoginRequiredMixin, SuccessUrlMixin,
                                 UsageCheckMixin as BaseUsageCheckMixin)


class RedirectUrlMixin:
    redirect_url = 'statuses'


class UsageCheckMixin(BaseUsageCheckMixin):
    message = _("Status can't be deleted because it's used in the task")


class ModelMixin:
    model = Status


class FormMixin:
    form_class = StatusForm


class IndexView(ModelMixin, LoginRequiredMixin, ListView):
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreateStatusView(FormMixin, ModelMixin, RedirectUrlMixin,
                       SuccessUrlMixin, LoginRequiredMixin,
                       SuccessMessageMixin, CreateView):
    template_name = 'statuses/create.html'
    success_message = _('Status creation was successful')


class UpdateStatusView(FormMixin, ModelMixin, RedirectUrlMixin,
                       SuccessUrlMixin, LoginRequiredMixin,
                       SuccessMessageMixin, UpdateView):
    template_name = 'statuses/update.html'
    success_message = _('Status has been updated')


class DeleteStatusView(ModelMixin, RedirectUrlMixin, SuccessUrlMixin,
                       LoginRequiredMixin, UsageCheckMixin,
                       SuccessMessageMixin, DeleteView):
    template_name = 'statuses/delete.html'
    success_message = _('Status has been deleted')
