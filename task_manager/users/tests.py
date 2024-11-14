from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _


class TestCreateUser(TestCase):

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
        self.new_user_login_data = {
            'username': 'test_username_new',
            'password': 'PsWd123*NeW'
        }

    def create_user(self, create_data=None):
        create_data = create_data or self.user_create_data
        return self.client.post(
            reverse('users_create'),
            data=create_data,
            follow=True
        )

    def login_user(self, login_data=None):
        login_data = login_data or self.user_login_data
        return self.client.post(
            reverse('login'),
            data=login_data,
        )

    def get_user_url(self, pk, url='users_update'):
        return reverse(url, kwargs={'pk': pk})

    def show_user(self, created_user):
        return self.client.get(
            self.get_user_url(created_user.pk),
        )

    def assert_user_data(self, response, username, first_name, last_name):
        self.assertContains(response, username)
        self.assertContains(response, first_name)
        self.assertContains(response, last_name)

    def test_create_user(self):
        users_count = User.objects.count()
        response = self.create_user()
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("Registration was successful")
        )

    def test_read_user(self):
        self.create_user()
        created_user = User.objects.last()
        self.login_user()
        response = self.show_user(created_user)
        self.assert_user_data(
            response,
            self.user_create_data['username'],
            self.user_create_data['first_name'],
            self.user_create_data['last_name']
        )

    def test_update_user(self):
        self.create_user()
        created_user = User.objects.last()
        self.login_user()
        response = self.client.post(
            self.get_user_url(created_user.pk),
            data=self.user_update_data,
            follow=True
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("User has been updated")
        )
        self.login_user(self.new_user_login_data)
        response = self.show_user(created_user)
        self.assert_user_data(
            response,
            self.user_update_data['username'],
            self.user_update_data['first_name'],
            self.user_update_data['last_name']
        )

    def test_delete_user(self):
        self.create_user()
        created_user = User.objects.last()
        self.login_user()
        response = self.client.post(self.get_user_url(
            created_user.pk,
            'users_delete'
        ))
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("User has been deleted")
        )
        response = self.client.get(reverse('users'))
        self.assertNotContains(
            response,
            f"{self.user_create_data['first_name']} "
            f"{self.user_create_data['last_name']}"
        )
