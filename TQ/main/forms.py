from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import *
from django.forms.utils import ErrorList
from .models import *
from django import forms


class EnterFormPhone(forms.Form):
    phone = forms.CharField(
        max_length=255,
        label="Введите номер телефона",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class EnterFormPassword(forms.Form):
    password = forms.CharField(
        max_length=4,
        label="На Ваш номер было отправленно сообщение с кодом. Введите этот код",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )


class InviteCodeForm(forms.Form):
    invite = forms.CharField(
        max_length=6,
        label="Введите инвайт код другого пользователя, чтобы добавить его в список",
        widget=TextInput(attrs={'class': 'form-control text-center'}),
    )
