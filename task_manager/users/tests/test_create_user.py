from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from task_manager.utils import get_users_create_data, get_message
from django.utils.translation import gettext_lazy as _


class TestCreateUser(TestCase):
    user_create_data = get_users_create_data()[0]

    def test_create_user(self):
        users_count = User.objects.count()
        response = self.client.post(
            reverse('users_create'),
            data=self.user_create_data,
            follow=True
        )
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertEqual(
            get_message(response),
            _("Registration was successful")
        )
