from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .decorators import anonymous_required
@login_required
def home(request):
    # Your home view logic here
    return render(request, 'home.html')


@anonymous_required
def redirect_to_login(request):
    return redirect('login')


@anonymous_required
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'messages': messages.get_messages(request)})


@anonymous_required
def signup_view(request):
    if request.method == 'POST':
        print('request_received')
        form = CustomUserCreationForm(request.POST)  # Use your custom form class here
        if form.is_valid():
            print('form validated')
            form.save()
            print('form saved')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print('user authenticated')
            if user is not None:
                login(request, user)
                print('user logged in')
                return redirect('home')  # Replace 'home' with your desired URL name
        else:
            for field, errors in form.errors.items():
                if field != 'password2':
                    for error in errors:
                        messages.error(request, f"{error}")
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()  # Use your custom form class here
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')