from django.urls import path
from .views import (
    LivreurRegisterView,
    LivreurTokenObtainPairView,
    register_view,
    login_view,
    logout_view,
)

urlpatterns = [
    path("api/register/", LivreurRegisterView.as_view(), name="register"),
    path("api/login/", LivreurTokenObtainPairView.as_view(), name="login"),
    path("register-page/", register_view, name="register-page"),
    path("login-page/", login_view, name="login-page"),
    path("logout/", logout_view, name="logout"),
]
