
from django.db import models
from django.contrib.auth.models import User #AbstractUser

# Create your models here.

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    account_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    pin = models.CharField(max_length=300, null=True)
    hide_balance = models.BooleanField(default=False)
    frozen = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    currency = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=200, null=True)
    profile_picture = models.ImageField(upload_to='picture', blank=True, null=True)
    date_birth = models.DateField(verbose_name="date of birth", blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    block = models.BooleanField(default=False)
    kyc = models.BooleanField(default=False)
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Transactions(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions') 
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(verbose_name='transaction time', null=True, blank=True)
    transaction_id = models.CharField(max_length=20)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __int__(self):
        return self.amount
    
class Loans(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    name = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Loan(models.Model):
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE, related_name='loan', blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    loanner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loanner', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='loaned time', auto_now=True)
    approve = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    days_count = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.loanner.username 
    
class Investments(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    name = models.TextField(blank=True, null=True)
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    duration = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Investment(models.Model):
    investment = models.ForeignKey(Investments, on_delete=models.CASCADE, related_name='investment', blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor')
    invested_on = models.DateTimeField(verbose_name='invested time', auto_now=True)
    # due_on = models.PositiveIntegerField(default=0, blank=True, null=True)
    due_time = models.PositiveIntegerField(default=0, blank=True, null=True)
    due = models.BooleanField(default=False)
    days_count = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.investor.username 
    
class OTPCode(models.Model):
    otp = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_receiver')
    created_at = models.DateTimeField(verbose_name='otp time', auto_now=True)

    def __str__(self):
        return self.otp
    
class Email(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_receiver')
    body = models.TextField()
    date = models.DateTimeField(verbose_name='sent time', auto_now=True)

    def __srt__(self):
        return self.receiver
    
