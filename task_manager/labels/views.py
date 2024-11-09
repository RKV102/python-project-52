from .models import Label
from .forms import LabelForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from task_manager.decorators import usage_check_decorator, rollbar_decorator
from task_manager.mixins import LoginRequiredMixin, BaseSuccessUrlMixin


REDIRECT_URL = 'labels'


class SuccessUrlMixin(BaseSuccessUrlMixin):
    redirect_url = REDIRECT_URL


class ModelMixin:
    model = Label


class FormMixin:
    form_class = LabelForm


class IndexView(ModelMixin, LoginRequiredMixin, ListView):
    template_name = 'labels/index.html'
    context_object_name = 'labels'


@method_decorator(rollbar_decorator, name='post')
class CreateLabelView(FormMixin, ModelMixin, SuccessUrlMixin,
                      LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'labels/create.html'
    success_message = _('Label creation was successful')


@method_decorator(rollbar_decorator, name='post')
class UpdateLabelView(FormMixin, ModelMixin, SuccessUrlMixin,
                      LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'labels/update.html'
    success_message = _('Label has been updated')


@method_decorator(rollbar_decorator, name='post')
@method_decorator(usage_check_decorator(
    model=Label,
    message_text=_("Label can't be deleted because it's used in the task"),
    redirect_url=REDIRECT_URL
), name='post')
class DeleteLabelView(ModelMixin, SuccessUrlMixin, LoginRequiredMixin,
                      SuccessMessageMixin, DeleteView):
    template_name = 'labels/delete.html'
    success_message = _('Label has been deleted')
