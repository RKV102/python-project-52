from django.urls import path
from .views import IndexView, CreateStatusView, UpdateStatusView, DeleteUserView


urlpatterns = [
    path('', IndexView.as_view(), name='statuses'),
    path('create/', CreateStatusView.as_view(), name='statuses_create'),
    path('<int:pk>/update/', UpdateStatusView.as_view(),
         name='statuses_update'),
    path('<int:pk>/delete/', DeleteUserView.as_view(), name='statuses_delete'),
]
