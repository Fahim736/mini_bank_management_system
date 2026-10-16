from django.db import models
from accounts.models import BankAccount

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    )

    account = models.ForeignKey(BankAccount, related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    receiver_account = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.account_number}"