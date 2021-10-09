from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model

import random
import re

User = get_user_model()
valid_email_pattern = '[\S]+@[\S]+\.[\S]'

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if user:
            auth.login(request, user)
            return redirect(request.GET.get('next', '/')) # NOTE: Allows redirects for login_required pages
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('/accounts/login')
    else:
        bookCover = getBookCover(request)
        return render(request, 'login.html', bookCover)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    """Creates a new user"""
    if request.method == 'POST':
        flag = False

        first_name=request.POST.get('first_name', '')
        last_name=request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not first_name:
            flag = True
            messages.info(request, 'Enter your first name')
        if not last_name:
            flag = True
            messages.info(request, 'Enter your last name')

        if not email:
            flag = True
            messages.info(request, 'Enter your email')
        elif not re.search(valid_email_pattern, email):
            flag = True
            messages.info(request, 'Enter a valid email address')
        elif User.objects.filter(email=email).exists():
            flag = True
            messages.info(request, 'Email taken')

        if not password1:
            flag = True
            messages.info(request, 'Enter your password')
        elif len(password1) < 6:
            flag = True
            messages.info(request, 'Passwords must be at least 6 characters')

        if not password2:
            flag = True
            messages.info(request, 'Re-enter your password')
        elif password1 != password2:
            flag = True
            messages.info(request, 'Passwords must match')

        if flag:
            return redirect(request.META['HTTP_REFERER'])
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password1)
            user.save()
            print('User created')
            return redirect('/accounts/login')
        
    else:
        bookCover = getBookCover(request)

        return render(request, 'register.html', bookCover)

# get book cover for login/register page
def getBookCover(request):

    bookCovers = [
        'styles/images/cover-images/midnight.jpg',
        'styles/images/cover-images/night.jpg',
        'styles/images/cover-images/wealth.jpg',
        'styles/images/cover-images/exile.jpg',
        'styles/images/cover-images/american.jpg'
    ]

    sample = random.sample(bookCovers, 1)

    response = {
        "cover": sample[0]
    }

    return response
