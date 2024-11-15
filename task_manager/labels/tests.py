from django.test import TestCase
from .models import Label
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _


class StatusTestCase(TestCase):

    def setUp(self):
        user_create_data = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password1': 'PsWd123*',
            'password2': 'PsWd123*'
        }
        user_login_data = {
            'username': 'test_username',
            'password': 'PsWd123*'
        }
        self.label_create_data = {
            'name': 'test_label_name'
        }
        self.label_update_data = {
            'name': 'test_label_name_new'
        }
        self.client.post(
            reverse('users_create'),
            data=user_create_data,
        )
        self.client.post(
            reverse('login'),
            data=user_login_data
        )

    def create_label(self):
        return self.client.post(
            reverse('labels_create'),
            data=self.label_create_data,
            follow=True
        )

    def test_create_status(self):
        labels_count = Label.objects.count()
        response = self.create_label()
        self.assertEqual(Label.objects.count(), labels_count + 1)
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("Label creation was successful")
        )

    def test_read_status(self):
        self.create_label()
        response = self.client.get(reverse('labels'))
        self.assertContains(
            response,
            self.label_create_data['name'],
        )

    def test_update_status(self):
        self.create_label()
        created_label = Label.objects.last()
        response = self.client.post(
            reverse(
                'labels_update',
                kwargs={'pk': created_label.pk}
            ),
            data=self.label_update_data,
            follow=True
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("Label has been updated")
        )
        response = self.client.get(reverse('labels'))
        self.assertContains(
            response,
            self.label_update_data['name'],
        )

    def test_delete_status(self):
        self.create_label()
        created_label = Label.objects.last()
        response = self.client.post(
            reverse(
                'labels_delete',
                kwargs={'pk': created_label.pk}
            ),
            data=self.label_update_data,
            follow=True
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[-1].message,
            _("Label has been deleted")
        )
        response = self.client.get(reverse('labels'))
        self.assertNotContains(
            response,
            self.label_create_data['name'],
        )
