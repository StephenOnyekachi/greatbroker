
from django.urls import path
from . import api_views

urlpatterns = [
    path("api_register/", api_views.register, name="api_register"),
    path("api_logout/", api_views.logout_api, name="api_logout"),
    path("api_login/", api_views.login_api, name="api_login"),
    path("dashboard/", api_views.dashboard, name="api_dashboard"),

    path("api_kyc/", api_views.kyc, name="api_kyc"),
    path("api_settings/", api_views.settings_view, name="api_settings"),
    path("api_update_picture/", api_views.update_picture, name="api_update_picture"),
    path("api_update_pin/", api_views.update_pin, name="api_update_pin"),
    path("api_update_password/", api_views.update_password, name="api_update_password"),
    path("api_transaction_history/", api_views.transaction_history, name="api_transaction_history"),

    path("api_allusers/", api_views.allUsers, name="api_allUsers"),
    path("api_transfer/", api_views.transfer, name="api_transfer"),
    path("api_transactions/", api_views.transactions, name="api_transactions"),

    path('api_loan_plans/', api_views.loan_plans, name="api_loan_plans"),
    path('api_apply_loan/', api_views.apply_loan, name="api_apply_loan"),
    path('api_user_loans/', api_views.user_loans, name="api_user_loans"),

    path('api_investment_plans/', api_views.investment_plans, name="api_investment_plans"),
    path('api_invest/', api_views.invest, name="invest"),
    path('api_user_investments/', api_views.user_investments, name="api_user_investments"),

]
