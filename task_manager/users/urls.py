from django.urls import path
from .views import IndexView, CreateUserView, UpdateUserView, DeleteUserView


urlpatterns = [
    path('', IndexView.as_view(), name='users'),
    path('create/', CreateUserView.as_view(), name='users_create'),
    path('<int:id>/update/', UpdateUserView.as_view(), name='users_update'),
    path('<int:id>/delete/', DeleteUserView.as_view(), name='users_delete'),
]
