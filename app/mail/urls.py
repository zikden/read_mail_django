from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('registration/', views.registration, name="registration"),
    path('mail/', views.mail, name="mail"),
]
