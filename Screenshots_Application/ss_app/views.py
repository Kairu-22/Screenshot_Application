from django.shortcuts import render,  redirect
import random
import time
import pyautogui
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, get_user_model

def index(request):
    if request.method == "POST":
        time.sleep(3)
        ss = pyautogui.screenshot()
        img = f'myimg{random.randint(1000,9999)}.png'
        ss.save(settings.MEDIA_ROOT/img)
        messages.success(request,'screenshot has been taken')
        return render(request,'index.html',{'img':img})
    
    return render(request,'index.html')

def signup(request):
    if not request.user.is_anonymous: #works when user is logged in 
        return redirect("/") 
    if request.method=="POST":

        User = get_user_model()
        users = User.objects.all()
        user_list=[]
        email_list=[]
        for i in users:
            user_list.append(i.username)
            email_list.append(i.email)

        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        if email in email_list:
            messages.error(request, 'Email already signed up. Head to login page.')
            return render(request,'signup.html')
        
        if name in user_list:
            messages.error(request, 'Username already Taken. Please try something else.')
            return render(request,'signup.html')
        
        user = User.objects.create_user(username=name, email=email, first_name=name, password=password)
        user.save()
        messages.success(request, f'Your account is created {name}. Head to login page!')
        
    return render(request,'signup.html')
