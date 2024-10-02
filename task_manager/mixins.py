from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from urllib.parse import urlsplit
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.utils.translation import gettext as _







