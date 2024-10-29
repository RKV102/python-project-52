from django.views.generic import ListView
from .models import Status
from .forms import StatusForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from task_manager.mixins import (LoginRequiredMixin, BaseUsageCheckMixin,
                                 BaseSuccessUrlMixin)


class SuccessUrlMixin(BaseSuccessUrlMixin):
    redirect_url = 'statuses'


class ModelMixin:
    model = Status


class FormMixin:
    form_class = StatusForm


class UsageCheckMixin(BaseUsageCheckMixin):
    message_text = _("Status can't be deleted because it's used in the task")
    redirect_url = 'statuses'


class IndexView(ModelMixin, LoginRequiredMixin, ListView):
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreateStatusView(FormMixin, ModelMixin, SuccessUrlMixin,
                       LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'statuses/create.html'
    success_message = _('Status creation was successful')


class UpdateStatusView(FormMixin, ModelMixin, SuccessUrlMixin,
                       LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'statuses/update.html'
    success_message = _('Status has been updated')


class DeleteStatusView(ModelMixin, SuccessUrlMixin, LoginRequiredMixin,
                       UsageCheckMixin, SuccessMessageMixin, DeleteView):
    template_name = 'statuses/delete.html'
    success_message = _('Status has been deleted')
