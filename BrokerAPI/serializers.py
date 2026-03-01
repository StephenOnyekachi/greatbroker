
from rest_framework import serializers
from django.contrib.auth.models import User
from BrokerApp.models import Wallet, Profile, Transactions, Loan, Loans, Investment, Investments



class WalletSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model = Wallet
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    wallet = WalletSerializer()
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name","last_name", "profile", "wallet"]


class TransactionSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Transactions
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

# Loan Plan
class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = "__all__"


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"

# Investment Plan
class InvestmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investments
        fields = "__all__"

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"



