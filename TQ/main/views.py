import random
import string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
    ListView,
    CreateView,
    FormView,
)
from django.middleware.csrf import get_token
from django.conf import settings


from .forms import *
from .serializers import UserSerializer

from smsru.service import SmsRuApi
from rest_framework import viewsets

import http
import requests

api = SmsRuApi()


# html страницы
def loginPage(request):
    return render(
        request,
        "main/login.html",
        {"form1": EnterFormPhone},
    )
    
@login_required
def profile(request):
    return render(request, "main/profile.html", {"form": InviteCodeForm()})

@login_required
def logoutUser(request):
    logout(request)
    return redirect("login")

# Функции
def phoneHTML(request):
    return HttpResponse(EnterFormPassword().as_p())
    

def phone(request):
    phone = request.POST["phone"]
    password = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    password_hash = make_password(password)
    
    result = api.send_one_sms(f"+{phone}", f"{password}")
    
    user = User.objects.filter(username = f"+{phone}")
    print(password)
    if len(user) > 0:
        user = User.objects.get(username = f"+{phone}")    
    else:
        user = User.objects.create(username = f"+{phone}")
    
    user.set_password(password)
    user.save()
    return HttpResponse(True)


def loginCode(request):
    phone = request.POST["phone"]
    password = request.POST["password"]
    
    user = User.objects.get(username = f"+{phone}")
    if user.check_password(password):
        if user.invite_code == "" or user.invite_code == "*":
            user.invite_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            user.save()
        
        
        auth_user = authenticate(request, username = f"+{phone}", password = password)
        print(auth_user)
        login(request, auth_user)
        
        success = JsonResponse({"success": "success"})
        success.status_code = 200
        return success
    else:
        error = JsonResponse({"error": "Неправильный код"})
        error.status_code = 401
        return error

@login_required
def findInvite(request):
    print(request)
    invite_code = request.POST["invite"]
    user = request.user
    try:
        user_invite = User.objects.get(invite_code = invite_code)
        invited = user_invite.invited.all()
        if user_invite not in invited and user_invite != user:
            user_invite.invited.add(user)
            return HttpResponse("Запрос успешно отправлен")
        else:
            error = JsonResponse({"error": True})
            error.status_code = 403
            
            return error
    except Exception as e:
        error = JsonResponse({"error": True})
        error.status_code = 404
        print(e)
        return error
    





# API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    










