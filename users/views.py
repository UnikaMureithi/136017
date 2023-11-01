from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserPredictionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def home(request):
    #return HttpResponse(request.user.user_type)
    if request.user.user_type == 'doctor':
        if request.method == 'POST':
            form = UserPredictionForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = UserPredictionForm()
        return render(request, 'users/prediction.html', {'form': form})
    else:
        return render(request, 'users/home.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def prediction(request):
    if request.method == 'POST':
        form = UserPredictionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserPredictionForm()

    return render(request, 'users/prediction.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                if user.user_type == 'patient':
                    #login(request, user)
                    return redirect('/prediction')  # Redirect patients to 'home'
                elif user.user_type == 'doctor':
                    login(request, user)
                    return redirect('prediction')  # Redirect doctors to 'prediction'
                else:
                    # Handle other roles or unknown users
                    pass
            else:
                # Handle inactive users
                pass
        else:
            # Handle invalid login
            pass

    return render(request, 'users/login.html')


##