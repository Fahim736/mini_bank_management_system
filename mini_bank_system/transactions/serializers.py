from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from transactions.models import Transaction


class DepositWithdrawSerializer(serializers.Serializer):
  account_number = serializers.CharField(max_length=20)
  amount = serializers.DecimalField(max_digits=12, decimal_places=2)

  def validate_amount(self, value):
    if value <= 0:
      raise serializers.ValidationError('পরিমাণ অবশ্যই শূন্য বা ঋণাত্মক হতে পারবে না।')
    return value


class TransferSerializer(serializers.Serializer):
  sender_account_number = serializers.CharField(max_length=20)
  receiver_account_number = serializers.CharField(max_length=20)
  amount = serializers.DecimalField(max_digits=12, decimal_places=2)

  def validate(self, data):
    if data['sender_account_number'] == data['receiver_account_number']:
      raise serializers.ValidationError(
          'একই অ্যাকাউন্টে টাকা ট্রান্সফার করা যাবে না।'
      )
    if data['amount'] <= 0:
      raise serializers.ValidationError('টাকার পরিমাণ শূন্য বা ঋণাত্মক হতে পারবে না।')
    return data


class TransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction
    fields = '__all__'