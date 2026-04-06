from django.urls import path
from .views import *
from .views import DepositView
from .views import WithdrawView
from .views import TransferView

urlpatterns = [
    path('create/', CreateAccountView.as_view()),
    path('me/', MyAccountView.as_view()),
    path('deposit/', DepositView.as_view()),
    path('withdraw/', WithdrawView.as_view()),
    # path('transactions/', TransactionHistoryView.as_view()),
    path('transfer/', TransferView.as_view()),
]