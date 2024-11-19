from .models import Label
from .forms import LabelForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (LoginRequiredMixin, SuccessUrlMixin,
                                 DeletionProtectedMixin as
                                 BaseDeletionProtectedMixin,
                                 ContextDataMixin)


class RedirectUrlMixin:
    redirect_url = 'labels'


class DeletionProtectedMixin(BaseDeletionProtectedMixin):
    message = _("Label can't be deleted because it's used in the task")


class ModelMixin:
    model = Label


class FormMixin:
    form_class = LabelForm


class IndexView(ModelMixin, LoginRequiredMixin, ListView):
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class CreateLabelView(FormMixin, ModelMixin, ContextDataMixin,
                      RedirectUrlMixin, SuccessUrlMixin, LoginRequiredMixin,
                      SuccessMessageMixin, CreateView):
    template_label_name = _('Creating label')
    url_name = 'labels_create'
    template_name = 'general/create.html'
    success_message = _('Label creation was successful')


class UpdateLabelView(FormMixin, ModelMixin, ContextDataMixin,
                      RedirectUrlMixin, SuccessUrlMixin, LoginRequiredMixin,
                      SuccessMessageMixin, UpdateView):
    template_label_name = _('Editing label')
    url_name = 'labels_update'
    template_name = 'general/update.html'
    success_message = _('Label has been updated')


class DeleteLabelView(ModelMixin, ContextDataMixin, RedirectUrlMixin,
                      SuccessUrlMixin, LoginRequiredMixin, SuccessMessageMixin,
                      DeletionProtectedMixin, DeleteView):
    template_label_name = _('Deleting label')
    url_name = 'labels_delete'
    template_name = 'general/delete.html'
    success_message = _('Label has been deleted')
