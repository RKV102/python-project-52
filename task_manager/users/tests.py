from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _


class UserTestCase(TestCase):

    def setUp(self):
        self.user_create_data = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password1': 'PsWd123*',
            'password2': 'PsWd123*'
        }
        self.user_login_data = {
            'username': 'test_username',
            'password': 'PsWd123*'
        }
        self.user_update_data = {
            'username': 'test_username_new',
            'first_name': 'test_first_name_new',
            'last_name': 'test_last_name_new',
            'password1': 'PsWd123*NeW',
            'password2': 'PsWd123*NeW'
        }

    def assert_user_data(self, response, first_assert, second_assert,
                         contains=True):
        if contains:
            self.assertContains(response, first_assert)
            self.assertContains(response, second_assert)
        else:
            self.assertNotContains(response, first_assert)
            self.assertNotContains(response, second_assert)

    def test_create_user(self):
        users_count = User.objects.count()
        response = self.client.post(
            reverse('users_create'),
            data=self.user_create_data,
            follow=True
        )
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("Registration was successful")
        )

    def test_read_user(self):
        self.client.post(
            reverse('users_create'),
            data=self.user_create_data,
            follow=True
        )
        response = self.client.get(reverse('users'))
        self.assert_user_data(
            response,
            self.user_create_data['username'],
            f"{self.user_create_data['first_name']} "
            f"{self.user_create_data['last_name']}"
        )

    def test_update_user(self):
        self.client.post(
            reverse('users_create'),
            data=self.user_create_data,
            follow=True
        )
        created_user = User.objects.last()
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('users_update', kwargs={'pk': created_user.pk}),
            data=self.user_update_data,
            follow=True
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("User has been updated")
        )
        response = self.client.get(reverse('users'))
        self.assert_user_data(
            response,
            self.user_update_data['username'],
            f"{self.user_update_data['first_name']} "
            f"{self.user_update_data['last_name']}"
        )

    def test_delete_user(self):
        self.client.post(
            reverse('users_create'),
            data=self.user_create_data,
            follow=True
        )
        created_user = User.objects.last()
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': created_user.pk})
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("User has been deleted")
        )
        response = self.client.get(reverse('users'))
        self.assert_user_data(
            response,
            self.user_create_data['username'],
            f"{self.user_create_data['first_name']} "
            f"{self.user_create_data['last_name']}",
            contains=False
        )
