from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserPredictionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import pickle
import xgboost as xgb
from .models import PredictionResult


# Load the XGBoost model
model_path = "C:/Users/unika/authsystem/authsysproject/models/xgboost_model.pkl"
with open(model_path, 'rb') as model_file:
    xgb_model = pickle.load(model_file)

def make_prediction(data):
    dmatrix = xgb.DMatrix(data)
    prediction = xgb_model.predict(dmatrix)
    return prediction

def home(request):
    #return HttpResponse(request.user.user_type)
    if hasattr(request.user,'user_type'):
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
    else:
        return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def prediction(request):
    if request.method == 'POST':
        form = UserPredictionForm(request.POST)
        if form.is_valid():
            # Get the form data and make predictions
            data = {
                'age': form.cleaned_data['age'],
                'height': form.cleaned_data['height'],
                'weight': form.cleaned_data['weight'],
                'gender': form.cleaned_data['gender'],
                'systolic_blood_pressure': form.cleaned_data['systolic_blood_pressure'],
                'diastolic_bp': form.cleaned_data['diastolic_bp'],
                'cholesterol': form.cleaned_data['cholesterol'],
                'glucose': form.cleaned_data['glucose'],
                'smoking_status': form.cleaned_data['smoking_status'],
                'alcohol_intake': form.cleaned_data['alcohol_intake'],
                'physical_activity': form.cleaned_data['physical_activity'],
            }
            prediction = make_prediction(data)

            # Save the prediction result in the database
            prediction_result = PredictionResult(prediction=prediction)
            prediction_result.save()

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