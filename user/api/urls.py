from django.urls import path
from .views import (
    registration_view,
    reset_password_view,
    authenticate_user,
)

app_name = "user"

urlpatterns = [
    path('/register', registration_view),  # http://127.0.0.1:8000/api/user/register
    path('/login', authenticate_user),
    path('/<int:user_id>/reset-password', reset_password_view),  # http://127.0.0.1:8000/api/user/14/reset-password
]