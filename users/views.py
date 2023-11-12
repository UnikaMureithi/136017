from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserPredictionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import xgboost as xgb
import pickle
import pandas as pd
import numpy as np
from .models import Result,Prediction
from django.contrib import messages 
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView




# Load the XGBoost model
model_path = "C:/Users/unika/authsystem/authsysproject/models/xgboost_model.pkl"
with open(model_path, 'rb') as model_file:
    xgb_model = pickle.load(model_file)

def make_prediction(data):
    try:
        # Convert categorical columns to numerical representations
        data['gender'] = '1' if data['gender'] == 'male' else '2'
        data['cholesterol'] = data['cholesterol'].encode('utf-8')
        data['glucose'] = data['glucose'].encode('utf-8')
        data['smoking_status'] = data['smoking_status'].encode('utf-8')
        data['alcohol_intake'] = data['alcohol_intake'].encode('utf-8')
        data['physical_activity'] = data['physical_activity'].encode('utf-8')

        # Create a NumPy array from the data
        features = np.array([[
            data['age'], data['height'], data['weight'], data['gender'],
            data['systolic_blood_pressure'], data['diastolic_bp'],
            data['cholesterol'], data['glucose'], data['smoking_status'],
            data['alcohol_intake'], data['physical_activity']
        ]])

        raw_prediction = xgb_model.predict(features)[0]
        prediction = int(raw_prediction > 0.5)  # Assuming a threshold of 0.5

        return prediction

    except Exception as e:
        print(f"Error in make_prediction: {e}")
        return None


# def home(request):
#     if hasattr(request.user, 'user_type') and request.user.user_type == 'doctor':
#         if request.method == 'POST':
#             form = UserPredictionForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('prediction')  # Redirect to the prediction page after saving the form
#         else:
#             form = UserPredictionForm()
#         return render(request, 'users/prediction.html', {'form': form})
#     else:
#         return render(request, 'users/home.html')

def home(request):
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


def prediction(request):
    prediction = None  # Initialize prediction variable

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
            raw_prediction = make_prediction(data)

            # Map raw prediction to human-readable labels
            prediction = "Presence of CVD" if raw_prediction == 1 else "Absence of CVD"

            # Save the prediction result in the database
            user_prediction = Prediction(**data)
            user_prediction.save()

            # Create a Result instance with the prediction
            prediction_result = Result(user=request.user, patient=user_prediction, prediction=prediction)
            prediction_result.save()

            # Add a success message with the prediction result
            messages.success(request, f'The prediction result is: {prediction}')

            # Redirect to the same page after successful prediction
            return redirect('prediction')

    else:
        form = UserPredictionForm()

    return render(request, 'users/prediction.html', {'form': form, 'prediction': prediction})




def profile(request):
    return render(request, 'users/profile.html')



class CustomLoginView(LoginView):
    def get_success_url(self):
        user_type = self.request.user.user_type

        if user_type == 'doctor':
            return reverse_lazy('prediction')
        else:
            return reverse_lazy('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                if user.user_type == 'patient':
                    login(request, user)
                    return redirect('home')  # Redirect patients to 'home'
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