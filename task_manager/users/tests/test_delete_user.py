from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, get_users_login_data


class TestDeleteUser(TestCase):
    user_login_data_1, user_login_data_2, *_ = get_users_login_data()

    def setUp(self):
        call_command('create_users')
        self.created_user = User.objects.last()

    def test_delete_user_by_unauthorized_user(self):
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.created_user.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_user_by_authorized_user(self):
        response = self.client.post(
            reverse('login'),
            data=self.user_login_data_2,
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.created_user.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("User has been deleted")
        )
        response = self.client.get(reverse('users'))
        self.assertNotContains(response, self.user_login_data_2['username'])

    def test_delete_user_by_another_user(self):
        response = self.client.post(
            reverse('login'),
            data=self.user_login_data_1,
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.created_user.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You don't have the rights to change another user")
        )
