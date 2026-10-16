from django.contrib.auth.models import User
from django.db import models


class BankAccount(models.Model):
  ACCOUNT_TYPES = (
      ('Savings', 'Savings'),
      ('Current', 'Current'),
  )

  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
  account_number = models.CharField(max_length=20, unique=True)
  account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
  balance = models.DecimalField(
      max_digits=12, decimal_places=2, default=0.00
  )  
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.account_number} - {self.user.username}'
