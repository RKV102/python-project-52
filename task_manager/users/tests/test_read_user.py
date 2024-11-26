from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User


class TestReadUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.last()

    def test_read_user(self):
        response = self.client.get(reverse('users'))
        self.assertContains(response, self.user.username)
