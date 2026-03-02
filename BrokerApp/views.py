
from django.http import HttpResponse,JsonResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db.models import Q, F
import random, time, datetime
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from . models import *

# for emails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

# deffine speruser function
def is_superuser(user):
    return user.is_superuser

# redirect user if not superuser
def CheckUser(view_func):
    decorated_view_funt= user_passes_test(
        is_superuser,
        login_url='dashboard',
        redirect_field_name=None
    )(view_func)
    return decorated_view_funt
    # user = request.user
    # if user.is_superuser:
    #     pass
    # return redirect('dashboard')

# for sending function
def SendMail(user):
    name = user
    email = user.email
    sender = 'sender@gmail.com'
    html_content = render_to_string(
        'extends/mail.html',
        {
            'name': name,
            'email': 'africeuros@gmail.com',
        }
    )
    message = EmailMultiAlternatives(
        subject = "Password Resting",
        body = html_content,
        from_email = sender,
        to = [f'{email}']
    )
    message.attach_alternative(html_content, 'text/html')
    message.send(fail_silently=False)

# sending otp code to the user email
def OTP(user):
    # for generation login otp code
    code = str(random.randint(0, 999999)).zfill(6)
    OTPCode.objects.create(
        otp=code,
        receiver=user
    )
    print('login code is', code)
    name = user
    email = user.email
    sender = 'sender@gmail.com'
    html_content = render_to_string(
        'extends/login-otp-mail.html',
        {
            'name': name,
            'email': 'africeuros@gmail.com',
            'code': code,
        }
    )
    message = EmailMultiAlternatives(
        subject = "Password Resting",
        body = html_content,
        from_email = sender,
        to = [f'{email}']
    )
    message.attach_alternative(html_content, 'text/html')
    message.send(fail_silently=False)

# for generating account number
def AccountNo():
    uni = '1100'
    rand1 = str(random.randint(100000, 999999))
    acc_number = uni + rand1
    return acc_number


# logout function
def Logout(request):
    user = request.user
    if user.is_superuser:
        logout(request)
        return redirect("login")
    logout(request)
    return redirect("login")

# login user user out after 24 hours
def AutoLogout(request, timeout_day = 1):
    # timeout_minues = timeout_hour * 60 # for 12 hour
    timeout_minues = timeout_day * 24 * 60 # for 24 hour
    now = datetime.datetime.now()
    try:
        last_activity = request.session['last_activity']
        last_activity = datetime.datetime.fromisoformat(last_activity)
        if(now - last_activity).total_seconds() / 60 > timeout_minues:
            logout(request)
    except KeyError:
        pass
    # request.session['last_active']=datetime.datetime.now()
    request.session['last_activity'] = now.isoformat()

# login function
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                # calling OPT functionn here
                # OTP(user)
                # loging in user after sending otp
                login(request, user)
                messages.success(request, f'{user.username}, Login successsfully')
                return redirect('adminPage')
            # calling OPT functionn here
            # OTP(user)
            # loging in user after sending otp
            login(request, user)
            messages.success(request, f'{user.username}, Login successsfully')
            return redirect('dashboard')
        messages.error(request, 'Incorrect username or password, please try again')
        return redirect('login')
    context={}
    return render(request,"landing/login.html",context)
    # return HttpResponse('welcome to django')

# user signup
def UserSignup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("mail")
        password2 = request.POST.get("password2")
        password1 = request.POST.get("password1")
        # calleing account number generator function
        acc_number = AccountNo()
        # verifing password
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email have been used, try another email')
                return redirect("signup")
            profile = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
            )
            Wallet.objects.create(
                user=profile,
                account_number=acc_number
            )
            Profile.objects.create(
                user=profile,
                info=password1,
            )
            # calling sehding mail functionn here after creating account
            # SendMail(profile)
            messages.success(request, f'you successfully created new user account "{first_name}"')
            return redirect("login")
        messages.success(request, f'password and confirm password are not matching try again')
        return redirect("signup")
    return render(request,"landing/signup.html")

def Index(request):
    context = {}
    return render(request, 'landing/landing.html', context)
    # return HttpResponse('welcome to django')

def About(request):
    context = {}
    return render(request, 'landing/about.html', context)
    # return HttpResponse('welcome to django')

def Features(request):
    context = {}
    return render(request, 'landing/features.html', context)
    # return HttpResponse('welcome to django')

def Contact(request):
    context = {}
    return render(request, 'landing/contact.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def Dashboard(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"
    picture = Profile.objects.get(user=user)
    block = Profile.objects.get(user=user)
    transactions = Transactions.objects.filter( 
        Q(sender=user) | Q(receiver=user) 
    ).order_by('-created_at')
    # Check if user has not set a pin
    investment = Investment.objects.filter( 
        Q(investor=user) and Q(due=False) 
    )
    if not wallet.pin:
        messages.warning(request, "You have not set your wallet pin yet. Please set it in your KYC before making any payments.")
    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'picture': picture.profile_picture,
        'transactions': transactions, 
        'user': user,
        'investment':investment,
        'total_investment': sum(int(amount.amount) for amount in investment),
        'investment_per': sum(int(invested.investment.interest) for invested in investment),
        'block':block,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def UserProfile(request):
    wallet = Wallet.objects.get(user=request.user)
    balance = f"{wallet.balance:,}"
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=request.user)
    picture = Profile.objects.get(user=request.user)
    context = {
        'balance':balance,
        'account_number':wallet.account_number,
        'user':user,
        'profile':profile,
        'picture':picture.profile_picture,
    }
    return render(request, 'profile.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def KYC(request):
    wallet = Wallet.objects.get(user=request.user)
    balance = f"{wallet.balance:,}"
    user = User.objects.get(username=request.user)
    kyc = Profile.objects.get(user=user)
    picture = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        pin = request.POST.get('pin')
        date = request.POST.get('date')
        image = request.FILES.get('image')
        profile = Profile.objects.get(user=user)
        if profile:
            profile.phone_number=phone
            profile.country=country
            # profile.currency
            profile.address=address
            profile.profile_picture=image
            profile.kyc=True
            profile.gender=gender
            profile.date_birth=date
            profile.save()
            messages.success(request, f'{user.username} your kyc have been varyfied')
            return redirect('kyc')
    context = {
        'balance':balance,
        'account_number':wallet.account_number,
        'user':user,
        'kyc':kyc,
        'picture':picture.profile_picture,
    }
    return render(request, 'kyc.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def Settings(request):
    wallet = Wallet.objects.get(user=request.user)
    balance = f"{wallet.balance:,}"
    user = User.objects.get(username=request.user)
    picture = Profile.objects.get(user=request.user)
    context = {
        'balance':balance,
        'account_number':wallet.account_number,
        'user':user,
        'picture':picture.profile_picture,
    }
    return render(request, 'setting.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def UpdatePicture(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        image = request.FILES.get("profilePicture")
        profile.profile_picture=image
        profile.save()
        messages.success(request, f'{request.user.username} your profile picture was updated successfully')
        return redirect('setting')
    
@login_required(login_url='login')
def UpdatePin(request):
    profile = Wallet.objects.get(user=request.user)
    if request.method == "POST":
        userpassword = request.POST.get('pass')
        pin = request.POST.get('npin')
        if request.user.check_password(userpassword):
            profile.pin = make_password(pin)
            profile.save()
            messages.success(request, f'{request.user.username} your pin was updated successfully')
            return redirect('setting')
        messages.success(request, f'{request.user.username} incorrect password, try agin')
        return redirect('setting')

@login_required(login_url='login')
def UpdatePassword(request):
    user = request.user
    if request.method == "POST":
        opassword = request.POST.get('opass')
        npassword = request.POST.get('npass')
        cnpassword = request.POST.get('cnpass')
        info = Profile.objects.get(user=request.user)
        if user.check_password(opassword):
            if npassword == cnpassword:
                user.set_password(npassword)
                user.save()
                info.info=npassword
                info.save()
                update_session_auth_hash(request, user)
                messages.success(request, f'{user.username} your password was updated successfully')
                return redirect('setting')
            else:
                messages.error(request, f'{user.username} two passwords do not match, try again')
                return redirect('setting')
        else:
            messages.error(request, f'{user.username} incorrect current old password, try again')
            return redirect('setting')

@login_required(login_url='login')
def History(request): 
    user = request.user 
    wallet = get_object_or_404(Wallet, user=user)
    balance = f"{wallet.balance:,}"
    picture = get_object_or_404(Profile, user=user) 
    transactions = Transactions.objects.filter( 
        Q(sender=user) | Q(receiver=user) 
    ).order_by('-created_at')
    context = { 
        'account_number': wallet.account_number, 
        'picture': picture.profile_picture,
        'balance': balance,
        'transactions': transactions, 
        'user': user, 
    } 
    return render(request, 'history.html', context)

@login_required(login_url='login')
def TransactionDetail(request, pk):
    transaction = get_object_or_404(Transactions, id=pk)
    # Security check: user must be sender or receiver
    if transaction.sender != request.user and transaction.receiver != request.user:
        return redirect('dashboard')
    context = {
        'transaction': transaction
    }
    return render(request, 'viewHistory.html', context)

@login_required(login_url='login')
def UserWithdraw(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"
    picture = Profile.objects.get(user=user)
    transactions = Transactions.objects.filter( 
        Q(sender=user) | Q(receiver=user) 
    ).order_by('-created_at')
    investment = Investment.objects.filter(investor=user)
    if request.method == 'POST':
        account = request.POST.get('account')
        # getting reciever account number from database
        try:
            reciever = Wallet.objects.get(account_number=account)
        except Wallet.DoesNotExist:
            messages.error(request, "Invalid account number.")
            return redirect('withdraw')
        if reciever:
            print('result is:', account, reciever.user)
            context = {
                'account':account,
            }
            return redirect('viewPayment', account=account)
        messages.error(request, f'{user.username} incorrect account number, please try again')
        return redirect('withdraw')
    context = {
        'balance':balance,
        'account_number':wallet.account_number,
        'picture':picture.profile_picture,
        'transactions': transactions, 
        'user': user,
        'investment':investment,
        'total_investment': sum(int(t.amount) for t in investment),
        'investment_per': sum(int(t.interest) for t in investment),
    }
    return render(request, 'withdraw.html', context)

@login_required(login_url='login')
def ViewPayment(request, account):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    receiver = get_object_or_404(Wallet, account_number=account)
    balance = f"{wallet.balance:,}"
    picture = Profile.objects.get(user=user)
    if request.method == "POST":
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        pin = request.POST.get('pin')
        if not pin:
            return render(request, 'extend/transaction_status.html', {
                'status': 'warning',
                'message': 'Please enter your PIN.'
            })
        if not wallet.pin:
            return render(request, 'extend/transaction_status.html', {
                'status': 'warning',
                'message': 'You have not set your transaction PIN yet.'
            })
        if check_password(pin, wallet.pin):
            # PIN correct → process payment
            return Pay(request, account, amount, description)
        else:
            # Wrong PIN
            return render(request, 'extend/transaction_status.html', {
                'status': 'error',
                'message': 'Incorrect PIN, try again.'
            })
    context = {
        'receiver': receiver,
        'balance': balance,
        'account_number': wallet.account_number,
        'picture': picture.profile_picture,
        'user': user,
        'account': account,
    }
    return render(request, 'varifyPayment.html', context)

@login_required(login_url='login')
def Pay(request, account, amount, description):
    code = str(random.randint(10, 99))
    transaction_id = str(code) + str(time.time())
    user = request.user
    try:
        # amount = Decimal(amount)
        amount = int(amount)
        if amount <= 0:
            return render(request, 'extend/transaction_status.html', {
                'status': 'warning',
                'message': 'Invalid amount.',
            })
    except:
        return render(request, 'extend/transaction_status.html', {
            'status': 'warning',
            'message': 'Invalid amount format.',
        })
    try:
        with transaction.atomic():
            sender = Wallet.objects.select_for_update().get(user=user)
            receiver_wallet = Wallet.objects.select_for_update().get(account_number=account)
            if sender.user == receiver_wallet.user:
                return render(request, 'extend/transaction_status.html', {
                    'status': 'warning',
                    'message': 'You cannot transfer to yourself.',
                })
            if sender.balance < amount:
                Transactions.objects.create(
                    sender=sender.user,
                    receiver=receiver_wallet.user,
                    amount=amount,
                    status='Failed',
                    transaction_id=transaction_id,
                    account_number=account,
                    description=description,
                    created_at=time.time(),
                )
                return render(request, 'extend/transaction_status.html', {
                    'status': 'error',
                    'message': 'Insufficient balance.',
                })
            # Update balances
            sender.balance -= amount
            receiver_wallet.balance += amount
            sender.save()
            receiver_wallet.save()
            # Log transaction
            Transactions.objects.create(
                sender=sender.user,
                receiver=receiver_wallet.user,
                amount=amount,
                status='Success',
                transaction_id=transaction_id,
                account_number=account,
                description=description,
                created_at=time.time(),
            )
    except Wallet.DoesNotExist:
        return render(request, 'extend/transaction_status.html', {
            'status': 'error',
            'message': 'Invalid account number.',
        })
    # Success
    return render(request, 'extend/transaction_status.html', {
        'status': 'success',
        'amount': amount,
        'reciever': receiver_wallet,
    })

@login_required(login_url='login')
def LoanApplication(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"
    picture = Profile.objects.get(user=user)
    loan = Loan.objects.filter( 
        Q(loanner=user) and Q(paid=False) 
    ).order_by('-created_at')
    loans = Loans.objects.all()
    if request.method == "POST":
        loan = request.POST.get('loan')
        amount =request.POST.get('amount')
        Loan.objects.create(
            loan_id = loan,
            loanner_id = user.id,
            amount = amount,
        )
        # wallet.balance += float(amount)
        # wallet.save()
        return render(request, 'extend/transaction_status.html', {
            'loan':'loan',
            'loan_status': 'pending',
            'amount': amount,
            'loanner': user,
        })
    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'picture': picture.profile_picture,
        'user': user,
        'total_loan': sum(int(loan.loan.amount) for loan in loan),
        'loans':loans,
    }
    return render(request, 'loanApplication.html', context)

@login_required(login_url='login')
def UserLoan(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"
    picture = Profile.objects.get(user=user)
    loan = Loan.objects.filter(loanner=user)
    notpaidloan = Loan.objects.filter( 
        Q(loanner=user) and Q(paid=False) 
    )
    paidloan = Loan.objects.filter( 
        Q(loanner=user) and Q(paid=True) 
    )
    if request.method == "POST":
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        Loan.objects.create(
            pay_back = duration,
            amount = amount,
            reason = description,
            loanner = user,
        )
        return render(request, 'extend/transaction_status.html', {
            'loan':'loan',
            'loan_status': 'pending',
            'amount': amount,
            'loanner': user,
        })
    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'picture': picture.profile_picture,
        'user': user,
        'loan':loan,
        'total_loan': sum(int(loan.loan.amount) for loan in notpaidloan),
        'paid_loan': sum(int(loan.loan.amount) for loan in paidloan),
    }
    return render(request, 'loan.html', context)

@login_required(login_url='login')
def AllInvestment(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"
    picture = Profile.objects.get(user=user)
    invested = Investment.objects.filter( 
        Q(investor=user) and Q(due=False) 
    )
    investments = Investments.objects.all()
    if request.method == "POST":
        investment = request.POST.get('investment')
        amount =request.POST.get('amount')
        interest =request.POST.get('interest')
        due_on =request.POST.get('due_on')
        with transaction.atomic():
            if wallet.balance >= (amount):
                wallet.balance -= (amount)
                wallet.save()
                Investment.objects.create(
                    investment_id = investment,
                    amount = amount,
                    investor_id = user.id,
                    due_on = due_on,
                )
                return render(request, 'extend/transaction_status.html', {
                    'status': 'success',
                    'amount': amount,
                    'reciever': user,
                })
            return render(request, 'extend/transaction_status.html', {
                'status': 'warning',
                'message': 'Invalid amount.',
            })
    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'picture': picture.profile_picture,
        'user': user,
        'total_invest': sum(int(invested.investment.amount) for invested in invested),
        'investments':investments,
    }
    return render(request, 'investments.html', context)

@login_required(login_url='login')
def UserInvestment(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"
    picture = Profile.objects.get(user=user)
    # investment = get_object_or_404(Investment, investor=user)
    investment = Investment.objects.filter(investor=user)
    dueinvestment = Investment.objects.filter( 
        Q(investor=user) and Q(due=False) 
    )
    # if dueinvestment:
    #     for days in dueinvestment:
    #         days = investment.objects.due_on - investment.days_count
    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'picture': picture.profile_picture,
        'user': user,
        'investment':investment,
        # 'remaining': day,
        'total_investment': sum(int(amount.amount) for amount in dueinvestment),
        'investment_per': sum(int(invested.investment.interest) for invested in dueinvestment),
    }
    return render(request, 'investment.html', context)

@login_required(login_url='login')
@CheckUser
def AdminPassword(request):
    user = request.user
    if request.method == "POST":
        opassword = request.POST.get('opass')
        npassword = request.POST.get('npass')
        cnpassword = request.POST.get('cnpass')
        if user.check_password(opassword):
            if npassword == cnpassword:
                user.set_password(npassword)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, f'{user.username} your password was updated successfully')
                return redirect('adminPassword')
            else:
                messages.error(request, f'{user.username} two passwords do not match, try again')
                return redirect('adminPassword')
        else:
            messages.error(request, f'{user.username} incorrect current old password, try again')
            return redirect('adminPassword')
    context ={}
    return render(request, 'admin/setting.html', context)

@login_required(login_url='login')
@CheckUser
def AdminPage(request):
    users = Wallet.objects.all()
    context = {
        'users':users,
    }
    return render(request, 'admin/adminPage.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
@CheckUser
def Search(request):
    if request.method == 'POST':
        query = request.POST.get('query','')
        user = Wallet.objects.filter(
            Q(account_number__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    context = {
        'query':user,
    }
    return render(request, 'admin/search.html', context)

@login_required(login_url='login')
@CheckUser
def DeleteUser(request,pk):
    useraccount = User.objects.get(id=pk)
    if useraccount:
        useraccount.delete()
        messages.success(request, f'{useraccount.username}, was deleted')
        return redirect('adminPage')

@login_required(login_url='login')
@CheckUser
def MakeAdmin(request,pk):
    useraccount = User.objects.get(id=pk)
    if useraccount.is_superuser:
        useraccount.is_superuser = False
        useraccount.save()
        messages.success(request, f'{useraccount.username}, accoun was disapproved to admin')
        return redirect('viewUser', pk=useraccount.id)
    useraccount.is_superuser = True
    useraccount.save()
    messages.success(request, f'{useraccount.username}, accoun was approved to admin')
    return redirect('viewUser', pk=useraccount.id)
    
@login_required(login_url='login')
@CheckUser
def BlockUser(request,pk):
    useraccount = User.objects.get(id=pk)
    profile = Profile.objects.get(user=useraccount)
    if profile.block:
        profile.block = False
        profile.save()
        messages.success(request, f'{useraccount.username}, accoun was unblock')
        return redirect('viewUser', pk=useraccount.id)
    profile.block = True
    profile.save()
    messages.success(request, f'{useraccount.username}, accoun was block')
    return redirect('viewUser', pk=useraccount.id)

@login_required(login_url='login')
@CheckUser
def AddBalace(request,pk):
    useraccount = User.objects.get(id=pk)
    if request.method == 'POST':
        balance = request.POST.get('balance')
        wallet = Wallet.objects.get(user=useraccount)
        if wallet:
            wallet.balance += int((balance))
            wallet.save()
            return redirect('viewUser', pk=wallet.user.id)
        
@login_required(login_url='login')
@CheckUser
def ClearBalace(request,pk):
    useraccount = User.objects.get(id=pk)
    wallet = Wallet.objects.get(user=useraccount)
    if wallet:
        wallet.balance = 0
        wallet.save()
        return redirect('viewUser', pk=wallet.user.id)

@login_required(login_url='login')
@CheckUser
def ViewUser(request,pk):
    useraccount = User.objects.get(id=pk)
    wallet = Wallet.objects.get(user=useraccount)
    balance = f"{wallet.balance:,}"
    accountNo = wallet.account_number
    profile = Profile.objects.get(user=useraccount)
    transaction = Transactions.objects.filter(
        Q(sender=useraccount) | Q(receiver=useraccount) 
    )
    context = {
        'useraccount':useraccount,
        'balance':balance,
        'accountNo':accountNo,
        'profile':profile,
        'transaction':transaction,
    }
    return render(request, 'admin/viewUsers.html', context)

@login_required(login_url='login')
@CheckUser
def CreateTransactions(request,pk):
    code = str(random.randint(10, 99))
    transaction_id = str(code) + str(time.time())
    sender = User.objects.get(id=pk)
    user = User.objects.get(id=pk)
    transactions = Transactions.objects.filter( 
        Q(sender=user) | Q(receiver=user) 
    ).order_by('-created_at')
    users = User.objects.filter(is_superuser=False)
    if request.method == 'POST':
        type = request.POST.get('type')
        person = request.POST.get('person')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')
        if person:
            account = Wallet.objects.get(user_id=person)
            if person == sender.id:
                print('correct',sender.id, person)
                messages.info(request, 'user selected can not be the same person with sender or receiver, try again')
                return redirect('createTransactions', pk=sender.id)
            else:
                print('wrong',sender.id, person)
                if type == 'sender':
                    Transactions.objects.create(
                        sender_id=sender.id,
                        receiver_id=person,
                        amount=amount,
                        status='Success',
                        transaction_id=transaction_id,
                        account_number=account.account_number,
                        description=description,
                        created_at=date,
                    )
                    messages.success(request, 'transaction created')
                    return redirect('viewUser', pk=sender.id)
                elif type == 'receiver':
                    Transactions.objects.create(
                        sender_id=person,
                        receiver_id=sender.id,
                        amount=amount,
                        status='Success',
                        transaction_id=transaction_id,
                        account_number=account.account_number,
                        description=description,
                        created_at=date,
                    )
                    messages.success(request, 'transaction created')
                    return redirect('viewUser', pk=sender.id)
    context = {
        'users':users,
        'sender':sender,
        'transactions':transactions,
    }
    return render(request, 'admin/createHistory.html', context)

@login_required(login_url='login')
@CheckUser
def DeleteUserTransactions(request,pk):
    transaction = Transactions.objects.get(id=pk)
    if transaction:
        transaction.delete()
        return redirect('adminPage')

@login_required(login_url='login')
@CheckUser
def DeleteTransactions(request,pk):
    useraccount = User.objects.get(id=pk)
    transaction = Transactions.objects.filter(
        Q(sender=useraccount) | Q(receiver=useraccount) 
    )
    if transaction:
        transaction.delete()
        return redirect('viewUser', pk=useraccount.id)

@login_required(login_url='login')
@CheckUser
def ViewUserLoan(request,pk):
    useraccount = User.objects.get(id=pk)
    wallet = Wallet.objects.get(user=useraccount)
    balance = f"{wallet.balance:,}"
    loan = Loan.objects.filter(loanner=useraccount)
    notpaidloan = Loan.objects.filter( 
        Q(loanner=useraccount) & Q(paid=False) 
    )
    paidloan = Loan.objects.filter( 
        Q(loanner=useraccount) & Q(paid=True) 
    )
    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'loan':loan,
        'total_loan': sum(int(loan.loan.amount) for loan in notpaidloan),
        'paid_loan': sum(int(loan.loan.amount) for loan in paidloan),
    }
    return render(request, 'admin/userLoan.html', context)

@login_required(login_url='login')
@CheckUser
def ApproveLoan(request,pk):
    loan = Loan.objects.get(id=pk)
    if loan:
        wallet = Wallet.objects.get(user=loan.loanner)
        wallet.balance += (loan.amount)
        wallet.save()
        loan.approve = True
        loan.save()
        return redirect('viewUserLoan', pk=wallet.user.id)
    
@login_required(login_url='login')
@CheckUser
def PaidLoan(request,pk):
    loan = Loan.objects.get(id=pk)
    if loan:
        wallet = Wallet.objects.get(user=loan.loanner)
        wallet.balance -= (loan.amount)
        wallet.save()
        loan.paid = True
        loan.save()
        return redirect('viewUserLoan', pk=wallet.user.id)
    
@login_required(login_url='login')
@CheckUser
def ViewUserInvestment(request,pk):
    useraccount = User.objects.get(id=pk)
    wallet = Wallet.objects.get(user=useraccount)
    balance = f"{wallet.balance:,}"
    investment = Investment.objects.filter(investor=useraccount)
    dueinvestment = Investment.objects.filter( 
        Q(investor=useraccount) & Q(due=False) 
    )
    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'investment':investment,
        'total_investment': sum(int(amount.amount) for amount in dueinvestment),
        'investment_per': sum(int(invested.investment.interest) for invested in dueinvestment),
    }
    return render(request, 'admin/userInvestment.html', context)

@login_required(login_url='login')
@CheckUser
def AddPercent(request,pk):
    investment = Investment.objects.get(id=pk)
    if investment:
        investment.amount += Decimal(investment.investment.interest)
        investment.days_count += 1
        investment.save()
        if investment.days_count == investment.due_time:
            investment.due = True
            investment.save()
        return redirect('viewUserInvestment', pk=investment.investor.id)
    
@login_required(login_url='login')
@CheckUser
def ReleaseInvestment(request,pk):
    investment = Investment.objects.get(id=pk)
    if investment:
        wallet = Wallet.objects.get(user=investment.investor)
        wallet.balance += (investment.amount)
        wallet.save()
        investment.due = True
        investment.save()
        return redirect('viewUserInvestment', pk=investment.investor.id)
    
@login_required(login_url='login')
@CheckUser
def NewInvestment(request):
    investments = Investments.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        interest = request.POST.get('interest')
        amount = request.POST.get('amount')
        Investments.objects.create(
            amount = amount,
            name = name,
            interest = interest,
        )
        messages.success(request, 'interest plan created successfully')
        return redirect('newInvestment')
    context = {
        'investments':investments,
    }
    return render(request,'admin/investment.html',context)

@login_required(login_url='login')
@CheckUser
def DeleteInvestment(request,pk):
    investment = Investments.objects.get(id=pk)
    if investment:
        investment.delete()
        messages.success(request, 'investment plan deleted successfully')
        return redirect('newInvestment')

@login_required(login_url='login')
@CheckUser
def NewLoan(request):
    loans = Loans.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        amount = request.POST.get('amount')
        Loans.objects.create(
            amount = amount,
            name = name,
            duration = duration,
        )
        messages.success(request, 'loan plan created successfully')
        return redirect('newLoan')
    context = {
        'loans':loans,
    }
    return render(request,'admin/loan.html',context)

@login_required(login_url='login')
@CheckUser
def DeleteLoan(request,pk):
    loan = Loans.objects.get(id=pk)
    if loan:
        loan.delete()
        messages.success(request, 'loan plan deleted successfully')
        return redirect('newLoan')
