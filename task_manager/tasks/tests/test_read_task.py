from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users


class TestReadTask(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        create_users()
        self.task = Task.objects.last()
        self.user = self.task.creator
        self.user_login_data = {
            'username': self.user.username,
            'password': 'PsWd123*'
        }

    def test_read_task_by_unauthorized_user(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_read_task_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, self.task.name)
