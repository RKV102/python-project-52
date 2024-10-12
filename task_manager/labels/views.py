from django.shortcuts import render, get_object_or_404, redirect
from .models import Label
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _


LABELS_URL = reverse_lazy('labels')


class UsageCheckMixin(AccessMixin):
    message_text = _("Label can't be deleted because it's used in the task")

    def dispatch(self, request, *args, **kwargs):
        label_id = kwargs['pk']
        label = get_object_or_404(self.model, id=label_id)
        if label.task_set.all():
            messages.error(
                request,
                self.message_text,
                extra_tags='danger'
            )
            return redirect('labels')
        return super().dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        statuses = Label.objects.all()
        return render(
            request,
            'labels/index.html',
            context={'labels': statuses}
        )


class CreateLabelView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ('name',)
    template_name = 'labels/create.html'
    success_url = LABELS_URL
    success_message = _('Creation was successful')


class UpdateLabelView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ('name',)
    template_name = 'labels/update.html'
    success_url = LABELS_URL
    success_message = _('Label has been updated')


class DeleteLabelView(LoginRequiredMixin, UsageCheckMixin, SuccessMessageMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = LABELS_URL
    success_message = _('Label has been deleted')
