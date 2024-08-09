from django.urls import path

from .views import get_user_profile

app_name = 'api_profiles'
urlpatterns = [
    path('profile', get_user_profile, name='profile')
]
