from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestUpdateUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        create_users()
        self.user_1, self.user_2, *_ = User.objects.order_by('-id')
        self.user_login_data = get_content('user_login.json')
        self.user_update_data = {
            'username': 'test_username_new',
            'first_name': 'test_first_name_new',
            'last_name': 'test_last_name_new',
            'password1': 'PsWd123*NeW',
            'password2': 'PsWd123*NeW'
        }

    def test_update_user_by_unauthorized_user(self):
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user_1.pk}),
            data=self.user_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_update_user_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user_1.pk}),
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
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user_2.pk}),
            data=self.user_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You don't have the rights to change another user")
        )
