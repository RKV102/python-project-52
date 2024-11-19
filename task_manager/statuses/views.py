from django.views.generic import ListView
from .models import Status
from .forms import StatusForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (LoginRequiredMixin, SuccessUrlMixin,
                                 DeletionProtectedMixin as
                                 BaseDeletionProtectedMixin,
                                 ContextDataMixin)


class RedirectUrlMixin:
    redirect_url = 'statuses'


class DeletionProtectedMixin(BaseDeletionProtectedMixin):
    message = _("Status can't be deleted because it's used in the task")


class ModelMixin:
    model = Status


class FormMixin:
    form_class = StatusForm


class IndexView(ModelMixin, LoginRequiredMixin, ListView):
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreateStatusView(FormMixin, ModelMixin, ContextDataMixin,
                       RedirectUrlMixin, SuccessUrlMixin, LoginRequiredMixin,
                       SuccessMessageMixin, CreateView):
    template_label_name = _('Creating status')
    url_name = 'statuses_create'
    template_name = 'general/create.html'
    success_message = _('Status creation was successful')


class UpdateStatusView(FormMixin, ModelMixin, ContextDataMixin,
                       RedirectUrlMixin, SuccessUrlMixin, LoginRequiredMixin,
                       SuccessMessageMixin, UpdateView):
    template_label_name = _('Editing status')
    url_name = 'statuses_update'
    template_name = 'general/update.html'
    success_message = _('Status has been updated')


class DeleteStatusView(ModelMixin, ContextDataMixin, RedirectUrlMixin,
                       SuccessUrlMixin, LoginRequiredMixin,
                       DeletionProtectedMixin, SuccessMessageMixin,
                       DeleteView):
    template_label_name = _('Deleting status')
    url_name = 'statuses_delete'
    template_name = 'general/delete.html'
    success_message = _('Status has been deleted')
