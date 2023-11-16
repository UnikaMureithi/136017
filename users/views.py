from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserPredictionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import xgboost as xgb
import pickle

import numpy as np
import pandas as pd

from .models import Result,Prediction
from django.contrib import messages 
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from sklearn.preprocessing import StandardScaler




# Load the model
with open('C:/Users/unika/authsystem/authsysproject/models/xgb_model.pkl', 'rb') as model_file:
    xgb_model = pickle.load(model_file)

# Load the scaler
with open('C:/Users/unika/authsystem/authsysproject/models/scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

def make_prediction(data):
    try:
        # Create a DataFrame from the form data
        features_df = pd.DataFrame(data, index=[0])

        # Apply the scaler to the features
        features_scaled = scaler.transform(features_df)

        # Make predictions using the loaded model
        prediction = xgb_model.predict(features_scaled)[0]

        return prediction

    except Exception as e:
        print(f"Error in make_prediction: {e}")
        return None

        


def prediction(request):
    prediction_result = None

    if request.method == 'POST':
        form = UserPredictionForm(request.POST)
        if form.is_valid():
            try:
                # Get the form data and make predictions
                data = {
                    'age': form.cleaned_data['age'],
                    'gender': form.cleaned_data['gender'],
                    'height': form.cleaned_data['height'],
                    'weight': form.cleaned_data['weight'],
                    'systolic': form.cleaned_data['systolic'],
                    'diastolic': form.cleaned_data['diastolic'],
                    'cholesterol': form.cleaned_data['cholesterol'],
                    'glucose': form.cleaned_data['glucose'],
                    'smoke': form.cleaned_data['smoke'],
                    'alcohol': form.cleaned_data['alcohol'],
                    'active': form.cleaned_data['active'],
                }

                # Make predictions
                raw_prediction = make_prediction(data)

                # Map raw prediction to human-readable labels
                prediction_result = "Presence of CVD" if raw_prediction == 1 else "Absence of CVD"

                # Save the prediction result in the database
                patient = form.cleaned_data['patient']
                user_prediction = Prediction(
                    patient=patient, 
                    doctor=request.user,
                    name=f"{patient.first_name} {patient.last_name}", 
                    **data
                )
                user_prediction.save()

                # Create a Result instance with the prediction
                prediction_result_instance = Result(doctor=request.user, patient=user_prediction, prediction=prediction_result)
                prediction_result_instance.save()

                # Add a success message with the prediction result
                messages.success(request, f'The prediction result is: {prediction_result}')

            except Exception as e:
                print(f"Error during prediction: {e}")
                messages.error(request, 'An error occurred during prediction. Please try again.')

            # Redirect to the same page after form submission
            return redirect('prediction')

    else:
        form = UserPredictionForm()

    return render(request, 'users/prediction.html', {'form': form, 'prediction': prediction_result})




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






def profile(request):
    return render(request, 'users/profile.html')

def about(request):
    return render(request, 'users/about.html')


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