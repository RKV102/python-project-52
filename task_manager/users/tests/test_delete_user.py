from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestDeleteUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        create_users()
        self.user_1, self.user_2, *_ = User.objects.order_by('-id')
        self.user_login_data = get_content('user_login.json')

    def test_delete_user_by_unauthorized_user(self):
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user_1.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_user_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user_1.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("User has been deleted")
        )
        response = self.client.get(reverse('users'))
        self.assertNotContains(response, self.user_login_data['username'])

    def test_delete_user_by_another_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user_2.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You don't have the rights to change another user")
        )
