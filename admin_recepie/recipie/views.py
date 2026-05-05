from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User,Recipie

# Create your views here.
def login_admin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        print(email,password   )
        user=authenticate(request,email=email,password=password)
        if user is not None and user.is_admin:
            login(request,user)
            return redirect('usermgt/')
    return render(request,'login.html')





def user_mgt(request):
    # get all users
    return render(request, 'usermgmt.html')


def content_mod(request):
    return render(request,'contentmod.html')


def user_profile(request, id):
    
    return render(request, 'viewuser.html')

def indi_recipie(request):
    
    return render(request,'recipieinfo.html')