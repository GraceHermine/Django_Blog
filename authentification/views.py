from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('uname')
        if User.objects.filter(email=email).exists():
            messages.warning(request,'email is already exists')
            return redirect('register')
        else:
            user = User(email=email,password=password,first_name=firstname,
            last_name=lastname,username=username)
            user.set_password(password)
            user.save()
            subject = 'About Registration'
            message = f'Hi ,You has been registered successfully on website.'
            email_from = 'sinturana250@gmail.com'
            rec_list = [email,]
            response = send_mail(
                subject,
                message,
                email_from,
                rec_list,
                fail_silently=False
            )
            print("UYFRUYYUBTYUTBYUTUYBGUN", response)

            messages.success(request, 'User has been sucessfully registered')
            return redirect('/')
    return render(request,'register.html')


def login_user(request):
    if request.method=='POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')



