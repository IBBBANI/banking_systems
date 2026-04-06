from rest_framework import generics, permissions
from .models import BankAccount
from .serializers import BankAccountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework import permissions
import random


# Create Account
class CreateAccountView(generics.CreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        if BankAccount.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Account already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            account_number=str(random.randint(100000000000, 999999999999))
        )

# Get Logged-in User Account
class MyAccountView(generics.RetrieveAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return BankAccount.objects.get(user=self.request.user)

# Deposit
class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            account = BankAccount.objects.get(user=request.user)
        except BankAccount.DoesNotExist:
            return Response({"error": "Account not found"})

        amount = request.data.get('amount')

        # ✅ Validate amount
        if not amount:
            return Response({"error": "Amount is required"})

        amount = Decimal(amount)

        if amount <= 0:
            return Response({"error": "Amount must be greater than 0"})

        # ✅ Update balance
        account.balance += amount
        account.save()

        # ✅ Save transaction
        Transaction.objects.create(
            user=request.user,
            account=account,
            transaction_type='DEPOSIT',
            amount=amount
        )

        return Response({
            "message": "Amount deposited successfully",
            "balance": account.balance
        })



# Withdraw
class WithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            account = BankAccount.objects.get(user=request.user)
        except BankAccount.DoesNotExist:
            return Response({"error": "Account not found"})

        amount = request.data.get('amount')

        # ✅ Validate amount
        if not amount:
            return Response({"error": "Amount is required"})

        amount = Decimal(amount)

        if amount <= 0:
            return Response({"error": "Amount must be greater than 0"})

        # ❗ Check balance
        if account.balance < amount:
            return Response({"error": "Insufficient balance"})

        # ✅ Deduct balance
        account.balance -= amount
        account.save()

        # ✅ Save transaction
        Transaction.objects.create(
            user=request.user,
            account=account,
            transaction_type='WITHDRAW',
            amount=amount
        )

        return Response({
            "message": "Amount withdrawn successfully",
            "balance": account.balance
        })


User = get_user_model()

class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_username = request.data.get('receiver')
        amount = request.data.get('amount')

        # ✅ Validate input
        if not receiver_username or not amount:
            return Response({"error": "Receiver and amount required"})

        amount = Decimal(amount)

        if amount <= 0:
            return Response({"error": "Amount must be greater than 0"})

        # ✅ Get sender account
        try:
            sender_account = BankAccount.objects.get(user=sender)
        except BankAccount.DoesNotExist:
            return Response({"error": "Sender account not found"})

        # ✅ Get receiver user
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"})

        # ❗ Prevent self transfer
        if sender == receiver:
            return Response({"error": "Cannot transfer to yourself"})

        # ✅ Get receiver account
        try:
            receiver_account = BankAccount.objects.get(user=receiver)
        except BankAccount.DoesNotExist:
            return Response({"error": "Receiver account not found"})

        # ❗ Check balance
        if sender_account.balance < amount:
            return Response({"error": "Insufficient balance"})

        # 💸 TRANSFER LOGIC
        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save()
        receiver_account.save()

        # ✅ Save sender transaction
        Transaction.objects.create(
            user=sender,
            account=sender_account,
            transaction_type='TRANSFER',
            amount=amount
        )

        # ✅ Save receiver transaction
        Transaction.objects.create(
            user=receiver,
            account=receiver_account,
            transaction_type='TRANSFER',
            amount=amount
        )

        return Response({
            "message": "Transfer successful",
            "sent_to": receiver_username,
            "amount": amount,
            "balance": sender_account.balance
        })