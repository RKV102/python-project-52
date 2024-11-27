# Менеджер задач

[Приложение](https://python-project-52-ntlu.onrender.com/) является системой управления задачами, подобной [Redmine](http://www.redmine.org/). Она позволяет ставить задачи, назначать исполнителей и менять их статусы.

## Запуск менеджера задач в локальной среде

Необходимо:

1. Установить:
   - Python версии, совместимой с 3.8
   - Poetry
2. Поместить в корень проекта текстовый файл .env, содержащий следующие строки:
   - DATABASE_URL = "Адрес базы данных" (опционально)
   - SECRET_KEY = "Защищённый ключ"
   - DEBUG = "True/False" (опционально)
   - ROLLBAR_TOKEN = "Токен для системы отслеживания ошибок" (опционально)
   - ROLLBAR_ENABLED = "True/False" (опционально)
3. Выполнить команду `poetry install` в корне проекта
4. Запустить веб сервер командой `poetry run python manage.py runserver`

## Статус непрерывной интеграции:
[![Actions Status](https://github.com/RKV102/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/RKV102/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/08a5b0ad5595154b59fd/maintainability)](https://codeclimate.com/github/RKV102/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/08a5b0ad5595154b59fd/test_coverage)](https://codeclimate.com/github/RKV102/python-project-52/test_coverage)