from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, MeView, ContactCreateView, ContactListView

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/',    TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/',  TokenRefreshView.as_view(),   name='token_refresh'),
    path('auth/me/',       MeView.as_view(),             name='me'),

    # Contact
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('contact/list/', ContactListView.as_view(), name='contact-list'),
]