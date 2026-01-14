from django.urls import path
from .views import (
    login_view,
    register_view,
    logout_view,
    home_view,
    profile_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
]
