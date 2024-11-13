from .models import Label
from .forms import LabelForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (LoginRequiredMixin, SuccessUrlMixin,
                                 UsageCheckMixin as BaseUsageCheckMixin)


class RedirectUrlMixin:
    redirect_url = 'labels'


class UsageCheckMixin(BaseUsageCheckMixin):
    message = _("Label can't be deleted because it's used in the task")


class ModelMixin:
    model = Label


class FormMixin:
    form_class = LabelForm


class IndexView(ModelMixin, LoginRequiredMixin, ListView):
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class CreateLabelView(FormMixin, ModelMixin, RedirectUrlMixin, SuccessUrlMixin,
                      LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'labels/create.html'
    success_message = _('Label creation was successful')


class UpdateLabelView(FormMixin, ModelMixin, RedirectUrlMixin, SuccessUrlMixin,
                      LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'labels/update.html'
    success_message = _('Label has been updated')


class DeleteLabelView(ModelMixin, RedirectUrlMixin, SuccessUrlMixin,
                      LoginRequiredMixin, SuccessMessageMixin, UsageCheckMixin,
                      DeleteView):
    template_name = 'labels/delete.html'
    success_message = _('Label has been deleted')
