from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                get_fixture_data, create_users)


class TestUpdateTask(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        create_users()
        self.user_login_data = get_users_login_data()[0]
        self.tasks_data = get_fixture_data('tasks.json')
        self.created_task = Task.objects.last()
        self.task_update_data = {
            'name': 'test_task_new',
            'status': self.created_task.status.id,
            'creator': self.created_task.creator.id,
            'executor': self.created_task.executor.id
        }

    def test_update_task_by_unauthorized_user(self):
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.created_task.pk}),
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
            reverse('tasks_update', kwargs={'pk': self.created_task.pk}),
            data=self.task_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Task has been updated")
        )
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, self.task_update_data['name'])
