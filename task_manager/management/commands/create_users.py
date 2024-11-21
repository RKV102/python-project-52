from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from task_manager.utils import get_users_create_data
from task_manager.users.models import User


class Command(BaseCommand):
    help = 'Create users'

    def handle(self, *args, **kwargs):
        users_data = get_users_create_data()
        for user_data in users_data:
            User.objects.create(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                id=user_data['id'],
                password=make_password(user_data['password1']),
            )
