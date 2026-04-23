from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.Signup, name='signup'),
    path('login/', views.UserLogin, name='login'),
    path('addrecipie/', views.create_recipe, name='addrecipie'),
]