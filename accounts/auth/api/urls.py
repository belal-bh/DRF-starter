from django.urls import path
from knox import views as knox_views
from .views import (
        LoginView,
        UserViewSet,
        UserSignUpView,
        PhoneVerifyAuthViewSet,
    )

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('phone', PhoneVerifyAuthViewSet, basename='phone')

app_name = 'api_auth'
urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='auth_signup'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
] + router.urls