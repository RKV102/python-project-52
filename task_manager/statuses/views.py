from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from .models import Status
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _


class IndexView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(
            request,
            'statuses/index.html',
            context={'statuses': statuses}
        )


class CreateStatusView(SuccessMessageMixin, CreateView):
    model = Status
    fields = ('name',)
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Creation was successful')


class UpdateStatusView(SuccessMessageMixin, UpdateView):
    model = Status
    fields = ('name',)
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status has been updated')


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status has been deleted')
