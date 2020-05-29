from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages


def base(request):
    return render(request, 'base.html')


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, "le nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'registration/login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')