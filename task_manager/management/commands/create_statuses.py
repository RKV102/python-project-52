from django.core.management.base import BaseCommand
from task_manager.utils import get_fixture_data
from task_manager.statuses.models import Status


class Command(BaseCommand):
    help = 'Create statuses'

    def handle(self, *args, **kwargs):
        statuses_data = get_fixture_data('statuses.json')
        for status_data in statuses_data:
            Status.objects.create(
                name=status_data['name'],
                id=status_data['id']
            )
