from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.UserLogin.as_view(), name='login_user'),
    path('register', views.Register.as_view(), name='register_user'),
    path('checkOtp', views.CheckOtp.as_view(), name='checkOtp_user'),
    path('logout', views.user_logout, name='logout_user'),
    path('addAddress', views.AddAddressView.as_view(), name='addAddress_user'),
]
