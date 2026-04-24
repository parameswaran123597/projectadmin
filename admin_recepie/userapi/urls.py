from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.Signup, name='signup'),
    path('login/', views.UserLogin, name='login'),
    path('addrecipie/', views.create_recipe, name='addrecipie'),
    path('passwordchg/', views.ChangePassword, name='passwordchg'),
    path('deleterec/', views.DeleteRecipie, name='deleterec'),
    path('listrec/', views.all_recipes, name='listrec'),
    path('recipe/<int:id>/', views.get_recipe, name='get-recipe'),
    path('editrecipie/<int:id>/', views.edit_recipe, name='edit-recipe'),
    path('myrecipies/', views.MyRecipies, name='my-recipes'),
    path('singlerecipie/<int:id>/', views.RecipieDetails, name='single-recipie'),
]