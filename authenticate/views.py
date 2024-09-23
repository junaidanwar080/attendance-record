from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate,get_user_model
from django.contrib.auth.models import User
from django.contrib import messages


User = get_user_model()


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/dashboard/')
        else:
            return redirect('/teacher_dashboard/')

    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('/dashboard/')
                else:
                    return redirect('/teacher_dashboard/')
            else:
                message = 'Account temporarily blocked.'
                messages.error(request, message)
        else:
            message = 'Invalid username or password.'
            messages.error(request, message)

    return render(request, 'login.html', {'message': message})

def user_logout(request):
    logout(request)
    return redirect('user_login')