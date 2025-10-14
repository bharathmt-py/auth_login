from django.urls import path
from .import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]