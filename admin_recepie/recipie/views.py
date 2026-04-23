from django.shortcuts import render

# Create your views here.
def login_admin(request):
    return render(request,'login.html')
def user_mgt(request):
    return render(request,'usermgmt.html')
def content_mod(request):
    return render(request,'contentmod.html')
def user_profile(request):
    return render(request,'viewuser.html')
def indi_recipie(request):
    return render(request,'recipieinfo.html')