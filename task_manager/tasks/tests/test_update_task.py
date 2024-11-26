from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users


class TestUpdateTask(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        create_users()
        self.task = Task.objects.last()
        self.user = self.task.creator
        self.user_login_data = {
            'username': self.user.username,
            'password': 'PsWd123*'
        }
        self.task_update_data = {
            'name': 'test_task_new',
            'status': self.task.status.id,
            'creator': self.task.creator.id,
            'executor': self.task.executor.id
        }

    def test_update_task_by_unauthorized_user(self):
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}),
            data=self.task_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_update_task_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}),
            data=self.task_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Task has been updated")
        )
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, self.task_update_data['name'])
