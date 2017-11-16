from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'lrapp/index.html', context)

def success(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'lrapp/success.html', context)

def login(request):
    attempt = User.objects.login(request.POST['email'], request.POST['password'])

    if 'errors' in attempt:
        for error in attempt['errors']:
            messages.error(request, error)
        return redirect('/')

    if 'user' in attempt:
        user = User.objects.get(email = request.POST['email'])
        print user
        messages.success(request, 'Successfully Logged in')
        request.session['first_name'] = attempt['user']['first_name']
        return redirect('/success')


def register(request):
    user_input = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'password_confirm': request.POST['password_confirm'],
    }

    attempt = User.objects.register(user_input)

    if 'errors' in attempt:
        for error in attempt['errors']:
            messages.error(request, error)

    if 'new_user' in attempt:
        messages.success(request, 'Successfully registered')
        request.session['first_name'] = attempt['new_user']['first_name']
        return redirect('/success')

    return redirect('/')
