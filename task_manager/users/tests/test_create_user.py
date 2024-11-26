from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from task_manager.utils import get_message
from django.utils.translation import gettext_lazy as _


class TestCreateUser(TestCase):
    user_create_data = {
        'username': 'test_username',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'password1': 'PsWd123*',
        'password2': 'PsWd123*'
    }

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
