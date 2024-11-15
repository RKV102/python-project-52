from django.test import TestCase
from .models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _


class TasksTestCase(TestCase):

    def setUp(self):
        user_create_data_1 = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password1': 'PsWd123*',
            'password2': 'PsWd123*',
        }
        user_create_data_2 = {
            'username': 'test_username_new',
            'first_name': 'test_first_name_new',
            'last_name': 'test_last_name_new',
            'password1': 'PsWd123*NeW',
            'password2': 'PsWd123*NeW'
        }
        user_login_data = {
            'username': 'test_username',
            'password': 'PsWd123*'
        }
        created_users = []
        for user_create_data in (user_create_data_1, user_create_data_2):
            self.client.post(
                reverse('users_create'),
                data=user_create_data,
            )
            created_users.append(User.objects.last())
        created_user_1, created_user_2 = created_users
        self.client.post(
            reverse('login'),
            data=user_login_data
        )
        created_status_1, created_status_2 = [
            Status.objects.create(name=status_name)
            for status_name in ('test_status_name', 'test_status_name_new')
        ]
        self.task_create_data = {
            'name': 'test_task_name',
            'description': 'test_task_description',
            'status': created_status_1.id,
            'creator': created_user_1.id,
            'executor': created_user_2.id,
        }
        self.task_update_data = {
            'name': 'test_task_name_new',
            'description': 'test_task_description_new',
            'status': created_status_2.id,
            'creator': created_user_1.id,
            'executor': created_user_1.id,
        }

    def get_message(self, response):
        messages = list(get_messages(response.wsgi_request))
        if messages:
            return messages[-1].message

    def test_create_task(self):
        tasks_count = Task.objects.count()
        response = self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data,
            follow=True
        )
        self.assertEqual(Task.objects.count(), tasks_count + 1)
        self.assertEqual(
            self.get_message(response),
            _("Task creation was successful")
        )

    def test_read_task(self):
        self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data
        )
        created_task = Task.objects.last()
        response = self.client.get(reverse(
            'tasks_show',
            kwargs={'pk': created_task.pk}
        ))
        self.assertContains(response, self.task_create_data['name'])

    def test_update_task(self):
        self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data
        )
        created_task = Task.objects.last()
        response = self.client.post(
            reverse(
                'tasks_update',
                kwargs={'pk': created_task.pk}
            ),
            data=self.task_update_data,
            follow=True
        )
        self.assertEqual(
            self.get_message(response),
            _("Task has been updated")
        )
        response = self.client.get(reverse(
            'tasks_show',
            kwargs={'pk': created_task.pk}
        ))
        self.assertContains(response, self.task_update_data['name'])

    def test_delete_task(self):
        self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data
        )
        created_task = Task.objects.last()
        response = self.client.post(
            reverse(
                'tasks_delete',
                kwargs={'pk': created_task.pk}
            ),
            data=self.task_update_data,
            follow=True
        )
        self.assertEqual(
            self.get_message(response),
            _("Task has been deleted")
        )
        response = self.client.get(reverse('tasks'))
        self.assertNotContains(response, self.task_create_data['name'])
