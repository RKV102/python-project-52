from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, get_users_login_data


class TestUpdateUser(TestCase):
    user_login_data_1, user_login_data_2, *_ = get_users_login_data()
    user_update_data = {
        'username': 'test_username_new',
        'first_name': 'test_first_name_new',
        'last_name': 'test_last_name_new',
        'password1': 'PsWd123*NeW',
        'password2': 'PsWd123*NeW'
    }

    def setUp(self):
        call_command('create_users')
        self.created_user = User.objects.last()

    def test_update_user_by_unauthorized_user(self):
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.created_user.pk}),
            data=self.user_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_update_user_by_authorized_user(self):
        response = self.client.post(
            reverse('login'),
            data=self.user_login_data_2,
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.created_user.pk}),
            data=self.user_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("User has been updated")
        )
        response = self.client.get(reverse('users'))
        self.assertContains(response, self.user_update_data['username'])

    def test_update_user_by_another_user(self):
        created_user_2, created_user_1 = User.objects.order_by('-id')[:2]
        self.client.post(
            reverse('login'),
            data=self.user_login_data_2,
        )
        response = self.client.post(
            reverse('users_update', kwargs={'pk': created_user_1.pk}),
            data=self.user_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You don't have the rights to change another user")
        )
