from django.test import TestCase
from django.urls import reverse
from task_manager.utils import get_users_create_data


class TestReadUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user_create_data = get_users_create_data()[0]

    def test_read_user(self):
        response = self.client.get(reverse('users'))
        self.assertContains(response, self.user_create_data['username'])
