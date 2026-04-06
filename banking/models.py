from django.db import models
from users.models import CustomUser

class BankAccount(models.Model):

    ACCOUNT_TYPE_CHOICES = [
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
        ('BUSINESS', 'Business'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account_number} - {self.account_type}"
    
    account_type = models.CharField(
    max_length=10,
    choices=ACCOUNT_TYPE_CHOICES,
    default='SAVINGS'   
)
    
class Transaction(models.Model):

    TRANSACTION_TYPE = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER', 'Transfer'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount}"