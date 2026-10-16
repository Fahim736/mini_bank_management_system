from django.urls import path
from .views import (
    TransactionListView,
    DepositView,
    WithdrawView,
)

urlpatterns = [
    path('history/', TransactionListView.as_view(), name='transaction-history'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
]