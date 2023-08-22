from django.urls import path, include, re_path
from rest_framework import routers
from django.contrib.auth.decorators import login_required


from . import views






urlpatterns = [
    # html страницы
    path("", views.loginPage, name = "login"),
    path("profile/", views.profile, name = "profile"),
    path("findInvite/", views.findInvite, name = "findInvite"),
    path('logout/', views.logoutUser, name="logout"),
    
    # API
    path('api/v1/users/', views.UserViewSetList.as_view()),
    path('api/v1/createUser/', views.UserViewSetCreate.as_view()),
    
    path('api/v1/login/', views.LoginView.as_view()),
    path('api/v1/logout/', views.LogoutView.as_view()),
    
    path('api-auth/v1/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Функции
    path("phoneHTML/", views.phoneHTML, name = "phoneHTML"),
    path("phone/", views.phone, name = "phone"),
    path("loginCode/", views.loginCode, name = "loginCode"),
    
]
