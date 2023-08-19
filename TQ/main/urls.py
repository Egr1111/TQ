from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # html страницы
    path("", views.loginPage, name = "login"),
    path("profile/", views.profile, name = "profile"),
    path("findInvite/", views.findInvite, name = "findInvite"),
    path('logout/', views.logoutUser, name="logout"),
    
    # API
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Функции
    path("phoneHTML/", views.phoneHTML, name = "phoneHTML"),
    path("phone/", views.phone, name = "phone"),
    path("loginCode/", views.loginCode, name = "loginCode"),
    
]
