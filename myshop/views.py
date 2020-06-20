from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from  django.contrib.auth.models import Group



def base(request):
    return render(request, 'base.html')


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            group1 = Group.objects.get(name="caissier").user_set.all()
            group2 = Group.objects.get(name="magasinier").user_set.all()
            group3 = Group.objects.get(name="administrateur").user_set.all()

            if user in group1:
                return redirect('index1')
            elif user in group2:
                return redirect('index2')
            elif user in group3:
                return redirect('index')
        else:
            messages.error(request, "le nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'registration/login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')