from django.urls import path, include
from .views import IndexView, CreateUserView


urlpatterns = [
    path('', IndexView.as_view(), name='users'),
    path('create/', CreateUserView.as_view(), name='create_user')
]
