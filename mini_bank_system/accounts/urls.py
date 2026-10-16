from django.urls import path
from accounts.views import (
    RegisterView,
    BankAccountListCreateView,
    UserProfileView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('accounts/', BankAccountListCreateView.as_view(), name='account-list-create'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]