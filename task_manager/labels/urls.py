from django.urls import path
from .views import IndexView, CreateLabelView, UpdateLabelView, DeleteLabelView


urlpatterns = [
    path('', IndexView.as_view(), name='labels'),
    path('create/', CreateLabelView.as_view(), name='labels_create'),
    path('<int:pk>/update/', UpdateLabelView.as_view(), name='labels_update'),
    path('<int:pk>/delete/', DeleteLabelView.as_view(), name='labels_delete'),
]
