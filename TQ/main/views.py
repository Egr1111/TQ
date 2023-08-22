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
from .serializers import UserSerializerView, UserSerializerAuth

from smsru.service import SmsRuApi
import rest_framework
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import views, generics, viewsets
from datetime import tzinfo, timedelta, datetime
import datetime

import phonenumbers


ZERO = timedelta(0)


class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()

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

    my_number = phonenumbers.parse(phone)
    if not phonenumbers.is_possible_number(my_number):
        error = JsonResponse({"error": "Неправильный номер"})
        error.status_code = 52
        return error

    user = User.objects.filter(username=f"+{phone}")
    print(password)
    if user.exists():
        user = User.objects.get(username=f"+{phone}")
    else:
        user = User.objects.create(username=f"+{phone}")

    user.last_code = datetime.datetime.now(utc)
    result = api.send_one_sms(f"{phone}", f"{password}")
    password = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

    user.set_password(password)
    user.last_code = datetime.datetime.now(utc)
    user.save()
    return HttpResponse(True)


def loginCode(request):
    phone = request.POST["phone"]
    password = request.POST["password"]
    time_now = datetime.datetime.now(utc)
    user = User.objects.get(username=f"+{phone}")
    if (time_now - user.last_code).seconds > 60:
        error = JsonResponse({"error": "Время вышло, отправьте запрос заново"})
        error.status_code = 504
        return error
    if not user.check_password(password):
        error = JsonResponse({"error": "Неправильный код"})
        error.status_code = 52
        return error
    if user.invite_code == "" or user.invite_code == None:
        user.invite_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

        user.save()

    auth_user = authenticate(request, username=f"+{phone}", password=password)
    print(auth_user)
    login(request, auth_user)

    success = HttpResponse(user.invite_code)
    return success


@login_required
def findInvite(request):
    print(request)
    invite_code = request.POST["invite"]
    user = request.user
    try:
        user_invite = User.objects.get(invite_code=invite_code)
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
class LoginView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializers = UserSerializerAuth
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.invited.all()
        else:
            return Response(
                {
                    "result": "Вам нужно авторизоваться. Для этого сделайте POST запрос по этому же url адресу, введя в значение 'username' свой номер телефона или создайте новый аккаунт, сделав POST запрос по адресу /createUser/, в 'username' свой номер телефона и снова отправив POST запрос по адресу /login/."
                }
            )
    
    def get(self, request, format=None):
        if request.user.is_authenticated:
            return Response({request.user.username: list(request.user.invited.all())})
        else:
            return Response(
                {
                    "result": "Вам нужно авторизоваться. Для этого сделайте POST запрос по этому же url адресу, введя в значение 'username' свой номер телефона или создайте новый аккаунт, сделав POST запрос по адресу /createUser/, в 'username' свой номер телефона и снова отправив POST запрос по адресу /login/."
                }
            )

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            time_now = datetime.datetime.now(utc)
            username = request.data["username"]
            user = User.objects.get(username=username)
            my_number = phonenumbers.parse(username)
            if not phonenumbers.is_possible_number(my_number):
                error = Response({"error": "Неправильный номер"}, status=52)
                return error
            if (time_now - user.last_code).seconds < 60:
                password = request.data["password"]
                login(
                    request,
                    authenticate(request, username=username, password=password),
                )
                return Response(
                    {"result": f"Пользователь {request.user.username} авторизован."}
                )
            else:
                random_code = "".join(
                    random.choices(
                        string.ascii_uppercase + string.digits,
                        k=4,
                    )
                )
                print(random_code)
                user.last_code = time_now
                user.set_password(random_code)
                user.save()
                result = api.send_one_sms(f"{username}", f"{random_code}")
                return Response(
                    {
                        "result": f"Код аутентификации выслан на номер {user.username}. У вас есть минута, чтобы ввести этот код в POST запрос по этому же адресу, добавив значение 'password' с кодом, иначе при повторном запросе будет выслан новый код."
                    }
                )
        else:
            return Response(
                {"result": f"Вы и так авторизованны, {request.user.username}."}
            )


class LogoutView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logout(request)
        return Response({"result": "Спасибо за то, что пользовались нашим API!"})


class UserViewSetList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerView
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class UserViewSetCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = UserSerializerView


    def post(self, request):
        username = request.data["username"]
        user = User.objects.filter(username=username)
        time_now = datetime.datetime.now(utc)
        my_number = phonenumbers.parse(username)
        if not phonenumbers.is_possible_number(my_number):
            error = Response({"error": "Неправильный номер"}, status=52)
            return error
        if user.exists():
            error = Response({"error": "Такой пользователь существует"}, status=400)
            return error
        user = User.objects.create(username=username)
        user.invite_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        user.save()
        return Response({"result": f"Пользователь {username} создан."})
