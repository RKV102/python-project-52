from django.contrib import admin
from django.urls import path, include
from .views import IndexView, LoginView


urlpatterns = [
    path('', IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
]
