from django.test import TestCase
from django.contrib.auth.models import User


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='test_username', password='PsWd123*')

    def test_user_can_be_created(self):
        assert User.objects.last().username == 'test_username'

    def test_user_can_be_updated(self):
        user = User.objects.last()
        user.first_name = 'test_name'
        user.save()
        assert User.objects.last().first_name == 'test_name'

    def test_user_can_be_deleted(self):
        User.objects.last().delete()
        assert not User.objects.all()
