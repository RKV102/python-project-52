from django.test import TestCase
from .models import Status


class StatusTestCase(TestCase):

    def setUp(self):
        Status.objects.create(name='test_status')

    def test_status_can_be_created(self):
        assert Status.objects.last().name == 'test_status'

    def test_status_can_be_updated(self):
        status = Status.objects.last()
        status.name = 'test_name'
        status.save()
        assert Status.objects.last().name == 'test_name'

    def test_status_can_be_deleted(self):
        Status.objects.last().delete()
        assert not Status.objects.all()
