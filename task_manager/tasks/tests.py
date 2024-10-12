from django.test import TestCase
from .models import Task, User, Status


class TaskTestCase(TestCase):

    def setUp(self):
        Task.objects.create(
            name='test_task',
            creator=User.objects.create(
                username='test_username',
                password='PsWd123*'
            ),
            status=Status.objects.create(name='test_status'),
            description=''
        )

    def test_task_can_be_created(self):
        assert Task.objects.last().name == 'test_task'

    def test_task_can_be_updated(self):
        task = Task.objects.last()
        task.name = 'test_name'
        task.save()
        assert Task.objects.last().name == 'test_name'

    def test_task_can_be_deleted(self):
        Task.objects.last().delete()
        assert not Task.objects.all()
