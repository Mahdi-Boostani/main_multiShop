import random
from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, RegisterForm, CheckOtpForm, AddressForm
from django.contrib.auth import authenticate, login, logout
import ghasedakpack
import requests
from random import randint
from .models import User, Otp, Address
from django.utils.crypto import get_random_string
from uuid import uuid4


# SMS = ghasedakpack.Ghasedak("9c583d6f91b880dfd7765588f4d247e19e334eecf29ff887be34026e233e34a25A7mErYwJmAKa8zF")
class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')

            else:
                form.add_error('phone', 'invalid user data')
        else:
            form.add_error('phone', 'invalid data')

        return render(request, 'account/login.html', context={'form': form})


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', context={'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            token = str(uuid4())
            print(randcode)
            # SMS.verification(
            #     {'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': randcode}
            # )

            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            return redirect(reverse('account:checkOtp_user') + f'?token={token}')
        else:
            form.add_error('phone', 'invalid data')

        return render(request, 'account/register.html', context={'form': form})


class CheckOtp(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/checkOtp.html', context={'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        instance = Otp.objects.get(token=token)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(token=token, code=cd['code']).exists():
                user, is_create = User.objects.get_or_create(phone=instance.phone)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                instance.delete()
                return redirect('/')
            else:
                form.add_error('phone', 'invalid data')

            return render(request, 'account/checkOtp.html', context={"form", form})


def user_logout(request):
    logout(request)
    return redirect('/')


class AddAddressView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = AddressForm()
            return render(request, 'account/addAddress.html', context={'from': form})

        return redirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            form = AddressForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                Address.objects.create(user=request.user, fullName=cd['fullName'], address=cd['address'],
                                       phone=cd['phone'], postal_code=cd['postal_code'], email=cd['email'])
                next_page = request.GET.get('next')
                print(next_page)
                if next_page:
                    return redirect(next_page)
            return render(request, 'home/index.html', context={'from': form})
        return redirect('/')
