from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
# from .forms import UserPredictionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


from django.contrib import messages

def home(request):
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

    return render(request, 'users/register.html', {'form':form})

# def prediction(request):
#     return render(request, 'users/prediction.html')

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

def logout(request):
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name='Patients').exists():
                login(request, user)
                return redirect('users/home.html')  # Replace with your patient's dashboard URL
            elif user.groups.filter(name='Doctors').exists():
                login(request, user)
                return redirect('users/prediction.html')  # Replace with your doctor's dashboard URL
            else:
                # Handle other roles or unknown users
                pass
        else:
            # Handle invalid login
            pass

    return render(request, 'login.html')


@login_required
def patient_dashboard(request):
    # Patient dashboard logic
    return render(request, 'users/home.html')

@login_required
def doctor_dashboard(request):
    # Doctor dashboard logic
    return render(request, 'users/prediction.html')