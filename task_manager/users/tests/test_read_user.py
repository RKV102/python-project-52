from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from task_manager.utils import get_users_create_data


class TestReadUser(TestCase):
    user_create_data = get_users_create_data()[0]

    def setUp(self):
        call_command('create_users')

    def test_read_user(self):
        response = self.client.get(reverse('users'))
        self.assertContains(response, self.user_create_data['username'])
