from django.urls import path
from .views import (
    login_view,
    register_view,
    affiliate_register_view,
    logout_view,
    home_view,
    profile_view,
    change_password_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("home/", home_view, name="home"),
    path("register/affiliate/", affiliate_register_view, name="register-affiliate"),
    path("profile/", profile_view, name="profile"),
    path("change-password/", change_password_view, name="change_password"),
]
