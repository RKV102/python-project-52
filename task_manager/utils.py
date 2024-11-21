from django.contrib.messages import get_messages
from task_manager.settings import BASE_DIR
import json


def get_message(response):
    messages = list(get_messages(response.wsgi_request))
    if messages:
        return messages[-1].message


def get_fixture_data(fixture_name='users.json'):
    user_fixture_path = str(BASE_DIR / 'task_manager' / 'fixtures'
                            / fixture_name)
    with open(user_fixture_path) as fixture:
        users_data = json.load(fixture)
    return [{'id': user_data['pk'], **user_data['fields']} for user_data
            in users_data]


def get_users_create_data():
    users_data = get_fixture_data()
    users_create_data = [
        {
            'username': user_data['username'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'password1': user_data['password'],
            'password2': user_data['password'],
            'id': user_data['id']
        } for user_data in users_data
    ]
    return users_create_data


def get_users_login_data():
    users_data = get_fixture_data()
    users_login_data = [
        {
            'username': user_data['username'],
            'password': user_data['password'],
        } for user_data in users_data
    ]
    return users_login_data
