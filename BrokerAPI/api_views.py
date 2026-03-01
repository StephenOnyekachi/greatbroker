
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction
from BrokerApp.models import Wallet, Transactions
from .serializers import *
from BrokerApp.views import AccountNo
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from BrokerApp.models import Profile, Loans, Investment, Investments
from rest_framework.authtoken.models import Token
from django.db.models import Q, F
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")
    if password1 != password2:
        return Response({
            "error": "Passwords do not match"
        })
    if User.objects.filter(username=username).exists():
        return Response({
            "error": "Username already exists"
        })
    if User.objects.filter(email=email).exists():
        return Response({
            "error": "Email already exists"
        })
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password1,
        first_name=first_name,
        last_name=last_name,
    )
    # Generate account number
    acc_number = AccountNo()
    Wallet.objects.create(
        user=user,
        account_number=acc_number
    )
    Profile.objects.create(
        user=user,
        info=password1
    )
    return Response({
        "message": "Account created successfully",
        "username": user.username
    })

# @api_view(['POST'])
# def logout_api(request):
#     logout(request)
#     return Response({"message": "Logged out"})
# or
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    # delete token
    Token.objects.filter(user=request.user).delete()
    # logout session
    logout(request)
    return Response({
        "message": "Logout successful"
    })

@api_view(['POST'])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error":"Invalid login"})
    # THIS logs the user into Django
    login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        "token":token.key,
        # "redirect": "/dashboard/",
    })
# {"username":"user1","password":"user1"}

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def allUsers(request):
    # serializer
    # users = User.objects.all()
    # user = UserSerializer(users, many=True)
    # return Response(user.data)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    profile = Profile.objects.get(user=user)
    # Format balance
    balance = f"{wallet.balance:,}"
    # Transactions
    transactions = Transactions.objects.filter(
        Q(sender=user) | Q(receiver=user)
    )
    transaction_serializer = TransactionSerializer(transactions, many=True)
    # Investments
    investments = Investment.objects.filter(
        Q(investor=user) & Q(due=False)
    )
    investment_serializer = InvestmentSerializer(investments, many=True)
    # Check pin
    setpin = None
    if not wallet.pin:
        setpin = "You have not set your wallet pin yet."
    data = {
        "username": user.username,
        "balance": balance,
        "account_number": wallet.account_number,
        "block": profile.block,
        "transactions": transaction_serializer.data,
        "investments": investment_serializer.data,
        "setpin": setpin,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    user = request.user
    wallet = Wallet.objects.filter(user=user).first()
    profile = Profile.objects.filter(user=user).first()
    balance = None
    if wallet:
        balance = f"{wallet.balance:,}"
    data = {
        "username": user.username,
        "email": user.email,
        "balance": balance,
        "account_number": wallet.account_number if wallet else None,
        "phone": profile.phone_number if profile else None,
        "country": profile.country if profile else None,
        "kyc": profile.kyc if profile else None,
    }
    return Response(data)

    # or 
    # serializer = UserProfileSerializer(request.user)
    # return Response(serializer.data)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def kyc(request):
    user = request.user
    wallet = Wallet.objects.filter(user=user).first()
    profile = Profile.objects.filter(user=user).first()
    if request.method == "POST":
        phone = request.data.get("phone")
        address = request.data.get("address")
        gender = request.data.get("gender")
        country = request.data.get("country")
        date = request.data.get("date")
        image = request.FILES.get("image")
        if not profile:
            return Response({"error": "Profile not found"}, status=404)
        profile.phone_number = phone
        profile.country = country
        profile.address = address
        profile.gender = gender
        profile.date_birth = date
        if image:
            profile.profile_picture = image
        profile.kyc = True
        profile.save()
        return Response({
            "message": "KYC verified successfully",
            "username": user.username
        })
    # GET request
    data = {
        "username": user.username,
        "balance": f"{wallet.balance:,}" if wallet else None,
        "account_number": wallet.account_number if wallet else None,
        "kyc": profile.kyc if profile else None,
        "phone": profile.phone_number if profile else None,
        "country": profile.country if profile else None,
        "picture": profile.profile_picture.url if profile and profile.profile_picture else None,
    }
    return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def settings_view(request):
    user = request.user
    wallet = Wallet.objects.filter(user=user).first()
    profile = Profile.objects.filter(user=user).first()
    data = {
        "username": user.username,
        "email": user.email,
        "balance": f"{wallet.balance:,}" if wallet else None,
        "account_number": wallet.account_number if wallet else None,
        "profile_picture": (
            profile.profile_picture.url
            if profile and profile.profile_picture
            else None
        ),
    }
    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_picture(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return Response({"error": "Profile not found"}, status=404)
    image = request.FILES.get("profilePicture")
    if not image:
        return Response({"error": "No image uploaded"}, status=400)
    profile.profile_picture = image
    profile.save()
    return Response({
        "message": "Profile picture updated successfully",
        "username": request.user.username,
        "image": profile.profile_picture.url
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_pin(request):
    wallet = Wallet.objects.filter(user=request.user).first()
    if not wallet:
        return Response({"error": "Wallet not found"}, status=404)
    user_password = request.data.get("pass")  # Current password
    new_pin = request.data.get("npin")        # New PIN
    if not user_password or not new_pin:
        return Response({"error": "Password and new PIN are required"}, status=400)
    if not new_pin.isdigit() or len(new_pin) not in [4,6]:
        return Response({"error": "PIN must be 4 or 6 digits"}, status=400)
    if request.user.check_password(new_pin):
        return Response({"error": "New PIN cannot match your account password"}, status=400)
    if not request.user.check_password(user_password):
        return Response({"error": "Incorrect password"}, status=400)
    wallet.pin = make_password(new_pin)
    wallet.save()
    return Response({
        "message": "Wallet PIN updated successfully",
        "username": request.user.username
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    old_password = request.data.get("opass")
    new_password = request.data.get("npass")
    confirm_password = request.data.get("cnpass")
    if not old_password or not new_password or not confirm_password:
        return Response({"error": "All password fields are required"}, status=400)

    if not user.check_password(old_password):
        return Response({"error": "Incorrect current password"}, status=400)
    if new_password != confirm_password:
        return Response({"error": "New passwords do not match"}, status=400)
    # Optional: enforce password rules (min length, complexity)
    # if len(new_password) < 8:
    #     return Response({"error": "Password must be at least 8 characters"}, status=400)
    user.set_password(new_password)
    user.save()
    # info.info=npassword
    # info.save()
    # Keep session alive for session authentication
    update_session_auth_hash(request, user)
    return Response({
        "message": "Password updated successfully",
        "username": user.username
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    user = request.user
    wallet = get_object_or_404(Wallet, user=user)
    profile = get_object_or_404(Profile, user=user)
    transactions = Transactions.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-created_at')
    # Serialize transactions
    transaction_serializer = TransactionSerializer(transactions, many=True)
    data = {
        "username": user.username,
        "account_number": wallet.account_number,
        "balance": f"{wallet.balance:,}",
        "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
        "transactions": transaction_serializer.data,
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):

    account = request.data.get("account_number")
    amount = float(request.data.get("amount"))

    sender_wallet = Wallet.objects.get(user=request.user)
    receiver_wallet = Wallet.objects.get(account_number=account)

    if sender_wallet.balance < amount:
        return Response({"error":"Insufficient balance"})

    with transaction.atomic():

        sender_wallet.balance -= amount
        receiver_wallet.balance += amount

        sender_wallet.save()
        receiver_wallet.save()

        Transactions.objects.create(
            sender=request.user,
            receiver=receiver_wallet.user,
            amount=amount,
            status="Success"
        )

    return Response({"message":"Transfer successful"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactions(request):

    tx = Transactions.objects.filter(
        sender=request.user
    ) | Transactions.objects.filter(
        receiver=request.user
    )

    serializer = TransactionSerializer(tx, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def loan_plans(request):
    loans = Loans.objects.all()
    serializer = LoansSerializer(loans, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_loan(request):

    serializer = LoanSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(loanner=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_loans(request):

    loans = Loan.objects.filter(loanner=request.user)

    serializer = LoanSerializer(loans, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def investment_plans(request):

    plans = Investments.objects.all()

    serializer = InvestmentsSerializer(plans, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invest(request):

    serializer = InvestmentSerializer(data=request.data)

    if serializer.is_valid():

        wallet = Wallet.objects.get(user=request.user)
        amount = serializer.validated_data['amount']

        if wallet.balance < amount:
            return Response({
                "error": "Insufficient balance"
            }, status=400)

        wallet.balance -= amount
        wallet.save()

        serializer.save(investor=request.user)

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_investments(request):

    investments = Investment.objects.filter(investor=request.user)

    serializer = InvestmentSerializer(investments, many=True)

    return Response(serializer.data)


