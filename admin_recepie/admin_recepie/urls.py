from django.contrib import admin
from django.urls import path,include
from recipie import views
from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [
    path('',views.login_admin),
  
    path('usermgt/',views.user_mgt),
    path('recipiemod/',views.content_mod),
    path('userinfo/',views.user_profile),
    path('recipieinfo/',views.indi_recipie),
    path('userapi/',include('userapi.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
