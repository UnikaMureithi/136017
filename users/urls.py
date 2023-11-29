from django.urls import path, include
from.import views
from users.views import CustomLoginView
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('prediction/', views.prediction, name='prediction'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html', redirect_authenticated_user=False), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('verify_otp/', views.verify_otp, name= 'verify_otp'),
    path('charts/', views.chart_view, name='charts'),

]