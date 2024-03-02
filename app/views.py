import os
import socket
import psutil
import platform
from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound, HttpResponse ,HttpResponseRedirect,JsonResponse,HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
import pyotp
from .models import OTPKey


def index(request):
    if request.user.is_authenticated:
        Account = request.user
        context = {
            'Account': Account,
        }
        return render(request, 'index.html', context)
    else:
        return redirect('/login')

def otp(request):
    user_groups = request.user.groups.all()

    if any(group.name == 'OTP' for group in user_groups):
        all_otp_keys = OTPKey.objects.all()
        all_otp_data = []

        for key in all_otp_keys:
            totp = pyotp.TOTP(key.secret_key)
            otp_data = {'account_name': key.account_name, 'otp_value': totp.now()}
            all_otp_data.append(otp_data)
    else:
        return HttpResponseForbidden("You are not authorized to view OTP keys.")

    return render(request, 'otp.html', {'otp_data_list': all_otp_data, 'secret_keys': all_otp_keys})

def login_view(request):
    error_message = ""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/')
        else:
            error_message = "帳號或密碼錯誤"
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')

def registerView(request):
    error_message = ""  # Initialize the variable here

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_check = request.POST["password_check"]
        email = request.POST["email"]
        user_exist = User.objects.filter(username=username).exists()

        if password != password_check:
            error_message = "密碼及密碼確認必須相同"
        elif user_exist:
            error_message = "該帳號己經存在，請使用別的帳號"
        else:
            user_info = User.objects.create_user(username=username, email=email, password=password)
            user_info.save()
            return redirect('/login')

    return render(request, 'register.html', {'error_message': error_message})

def server_info(request):
    host_name=platform.node()
    os_name=platform.system()
    os_version=platform.release()
    processor=platform.processor()
    current_directory=os.getcwd()
    memory=psutil.virtual_memory()
    total_ram=memory.total
    internal_ipv4=socket.gethostbyname(socket.gethostname())
    context = {
        'host_name':host_name,
        'os_name':os_name,
        'os_version':os_version,
        'processor': processor,
        'current_directory':current_directory,
        'total_ram':total_ram,
        'internal_ipv4':internal_ipv4,}
    return render(request,'server_info.html',context)