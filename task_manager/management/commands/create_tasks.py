from django.core.management.base import BaseCommand
from task_manager.utils import get_fixture_data
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Command(BaseCommand):
    help = 'Create tasks'

    def handle(self, *args, **kwargs):
        tasks_data = get_fixture_data('tasks.json')
        for task_data in tasks_data:
            status_object = Status.objects.get(
                pk=task_data['status'])
            creator_object = User.objects.get(
                pk=task_data['creator'])
            executor_object = User.objects.get(
                pk=task_data['executor'])

            task = Task.objects.create(
                name=task_data['name'],
                description=task_data['description'],
                status=status_object,
                creator=creator_object,
                executor=executor_object,
            )
            task.labels.set(task_data['labels'])
            task.save()
