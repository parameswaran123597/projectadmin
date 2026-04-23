from django.contrib import admin
from django.urls import path,include
from recipie import views

urlpatterns = [
    path('login/',views.login_admin),
    path('usermgt/',views.user_mgt),
    path('recipiemod/',views.content_mod),
    path('userinfo/',views.user_profile),
    path('recipieinfo/',views.indi_recipie),
    path('userapi/',include('userapi.urls')),
]
