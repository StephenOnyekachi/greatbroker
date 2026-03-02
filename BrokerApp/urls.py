
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('about/', views.About, name='about'),
    path('features/', views.Features, name='features'),
    path('contact/', views.Contact, name='contact'),
    path('login/', views.UserLogin, name='login'),
    path('signup/', views.UserSignup, name='signup'),

    path('dashboard/', views.Dashboard, name='dashboard'),
    path('profile/', views.UserProfile, name='profile'),
    path('kyc/', views.KYC, name='kyc'),

    path('setting/', views.Settings, name='setting'),
    path('picture/', views.UpdatePicture, name='picture'),
    path('pin/', views.UpdatePin, name='pin'),
    path('password/', views.UpdatePassword, name='password'),

    path('history/', views.History, name='history'),
    path('transactionDetail/<str:pk>/', views.TransactionDetail, name='transactionDetail'),
    path('withdraw/', views.UserWithdraw, name='withdraw'),
    path('viewPayment/<int:account>/', views.ViewPayment, name='viewPayment'),
    path('pay/', views.Pay, name='pay'),

    path('loanApplication/', views.LoanApplication, name='loanApplication'),
    path('loan/', views.UserLoan, name='loan'),
    path('allInvestment/', views.AllInvestment, name='allInvestment'),
    path('investment/', views.UserInvestment, name='investment'),

    path('adminPassword/', views.AdminPassword, name='adminPassword'),
    path('adminPage/', views.AdminPage, name='adminPage'),
    path('search/', views.Search, name='search'),
    path('deleteUser/<int:pk>/', views.DeleteUser, name='deleteUser'),
    path('viewUser/<int:pk>/', views.ViewUser, name='viewUser'),
    path('blockUser/<int:pk>/', views.BlockUser, name='blockUser'),
    path('makeAdmin/<int:pk>/', views.MakeAdmin, name='makeAdmin'),

    path('addBalace/<int:pk>/', views.AddBalace, name='addBalace'),
    path('clearBalace/<int:pk>/', views.ClearBalace, name='clearBalace'),

    path('viewUserLoan/<int:pk>/', views.ViewUserLoan, name='viewUserLoan'),
    path('approveLoan/<int:pk>/', views.ApproveLoan, name='approveLoan'),
    path('paidLoan/<int:pk>/', views.PaidLoan, name='paidLoan'),

    path('viewUserInvestment/<int:pk>/', views.ViewUserInvestment, name='viewUserInvestment'),
    path('addPercent/<int:pk>/', views.AddPercent, name='addPercent'),
    path('releaseInvestment/<int:pk>/', views.ReleaseInvestment, name='releaseInvestment'),

    path('createTransactions/<int:pk>/', views.CreateTransactions, name='createTransactions'),
    path('deleteTransactions/<int:pk>/', views.DeleteTransactions, name='deleteTransactions'),
    path('deleteUserTransactions/<int:pk>/', views.DeleteUserTransactions, name='deleteUserTransactions'),

    path('newInvestment/', views.NewInvestment, name='newInvestment'),
    path('deleteInvestment/<int:pk>/', views.DeleteInvestment, name='deleteInvestment'),

    path('newLoan/', views.NewLoan, name='newLoan'),
    path('deleteLoan/<int:pk>/', views.DeleteLoan, name='deleteLoan'),
]
