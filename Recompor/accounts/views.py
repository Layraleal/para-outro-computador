from django.shortcuts import render, redirect
from .admin import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User 
from composteira import models

#ignora tudo q ta aq:)

# Create your views here.
def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('mysite')

        else:
            print('invalid registration details')
            
    return render(request, "registration/register.html",{"form": form})


def login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        #Função do django que autentica o usuário
        user = authenticate(username = username, password = senha)

        if user:
            login(request, user)
            #colocar Autenticado e renderizar a página do gráfico geral (com filtragem de composteira)
            composteiras = models.Composteira.objects.filter(fkUsuario_id = request.user)
            return render(request, "grafico-geral.html", {"composteiras": composteiras})

        else:
            #colocar mensagem que é preciso fazer o login 
            return render(request, "accounts/login.html") 
        
def deslogar(request):
    logout(request)
    messages.success(request, "Logout efetuado com sucesso!")
