from django.core.management.base import BaseCommand
from task_manager.utils import get_fixture_data
from task_manager.labels.models import Label


class Command(BaseCommand):
    help = 'Create labels'

    def handle(self, *args, **kwargs):
        labels_data = get_fixture_data('labels.json')
        for label_data in labels_data:
            Label.objects.create(
                name=label_data['name'],
                id=label_data['id']
            )
