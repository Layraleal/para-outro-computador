from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path("login/", views.login, name = "logar"),
    path("register", views.register, name="register"), 
    path('deslogar/',views.deslogar,name='deslogar'),
] 