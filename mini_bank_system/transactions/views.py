from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import BankAccount
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        user_accounts = BankAccount.objects.filter(user=self.request.user)
        return Transaction.objects.filter(account__in=user_accounts)



class DepositView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        account_number = request.data.get('account_number')
        amount = float(request.data.get('amount', 0))

        if amount <= 0:
            return Response({'error': 'টাকার পরিমাণ শূন্য বা ঋণাত্মক হতে পারবে না।'}, status=status.HTTP_400_BAD_REQUEST)

        account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

        
        account.balance += amount
        account.save()

        
        transaction = Transaction.objects.create(
            account=account,
            transaction_type='Deposit',
            amount=amount,
            balance_after_transaction=account.balance
        )

        serializer = self.get_serializer(transaction)
        return Response({'message': 'সফলভাবে ডিপোজিট করা হয়েছে।', 'data': serializer.data}, status=status.HTTP_201_CREATED)


class WithdrawView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        account_number = request.data.get('account_number')
        amount = float(request.data.get('amount', 0))

        if amount <= 0:
            return Response({'error': 'টাকার পরিমাণ সঠিক নয়।'}, status=status.HTTP_400_BAD_REQUEST)

        account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

        if account.balance < amount:
            return Response({'error': 'পর্যাপ্ত ব্যালেন্স নেই!'}, status=status.HTTP_400_BAD_REQUEST)

    
        account.balance -= amount
        account.save()

        
        transaction = Transaction.objects.create(
            account=account,
            transaction_type='Withdrawal',
            amount=amount,
            balance_after_transaction=account.balance
        )

        serializer = self.get_serializer(transaction)
        return Response({'message': 'সফলভাবে টাকা তোলা হয়েছে।', 'data': serializer.data}, status=status.HTTP_201_CREATED)