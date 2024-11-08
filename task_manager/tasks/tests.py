from django.test import TestCase
from .models import Task, User, Status
from .filters import TaskFilter


class TaskTestCase(TestCase):

    def setUp(self):
        status1 = Status.objects.create(name='status1')
        status2 = Status.objects.create(name='status2')
        creator1 = User.objects.create(
            username='username1',
            password=''
        )
        creator2 = User.objects.create(
            username='username2',
            password=''
        )
        creator3 = User.objects.create(
            username='username3',
            password=''
        )
        Task.objects.create(
            name='task1',
            creator=creator1,
            status=status1,
        )
        Task.objects.create(
            name='task2',
            creator=creator2,
            status=status2,
            executor=creator3
        )
        Task.objects.create(
            name='task3',
            creator=creator1,
            status=status1,
            executor=creator2
        )

    def test_task_can_be_created(self):
        assert Task.objects.last().name == 'task3'

    def test_task_can_be_updated(self):
        task = Task.objects.last()
        task.name = 'test_name'
        task.save()
        assert Task.objects.last().name == 'test_name'

    def test_task_can_be_deleted(self):
        Task.objects.last().delete()
        assert Task.objects.count() == 2

    def test_filter_task_by_status(self):
        status = Status.objects.get(name='status1')
        filter = TaskFilter({'status': status})
        filtered_tasks = filter.qs
        assert len(filtered_tasks) == 2
        assert all([task.status == status for task in filtered_tasks])

    def test_filter_task_by_executor(self):
        executor = User.objects.get(username='username3')
        filter = TaskFilter({'executor': executor})
        filtered_tasks = filter.qs
        assert len(filtered_tasks) == 1
        assert filtered_tasks.last().executor == executor

    def test_filter_task_by_status_and_executor(self):
        status = Status.objects.get(name='status1')
        executor = User.objects.get(username='username2')
        filter = TaskFilter({'status': status, 'executor': executor})
        filtered_tasks = filter.qs
        task = filtered_tasks.last()
        assert len(filtered_tasks) == 1
        assert task.status == status and task.executor == executor
