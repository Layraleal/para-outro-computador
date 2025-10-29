
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from composteira import models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from accounts.models import Perfil  # ajuste para o local do seu modelo Perfil

# Create your views here.


def entrar(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        foto = request.POST.get("foto") or "icon_user.png"  # Define a imagem padrão

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe.")
            return redirect("usuarios:entrar")

        # Cria o usuário
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        # Verifica se o perfil já existe
        perfil, criado = Perfil.objects.get_or_create(user=user)
        if not criado:
            perfil.foto = foto  # Atualiza a foto se o perfil já existir
        else:
            perfil.foto = foto  # Define a foto para o novo perfil
        perfil.save()

        return redirect("usuarios:logar")

    return render(request, "usuarios/cadastro.html")



def logarconta(request):
    if request.user.is_authenticated == True:
        #Verifica se o metodo é o get e não o post
        if request.method == 'GET': 
            return render(request, 'usuarios/conta.html')
        #Captura os dados e salva e renderiza para outra tela
        else:
            None
    return render(request, "usuarios/Login.html")   

def logar(request):
    if request.method == 'GET':
        return render(request, 'usuarios/Login.html')
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
            return render(request, "usuarios/login.html") 

# Função da deslogar usuário
def deslogar(request):
    logout(request)  
    messages.success(request, "Logout efetuado com sucesso!") 
    return redirect("paginas:home")  

def esqueceuSenha(request):
    if request.method == 'GET':
        return render(request, 'usuarios/Login.html')
    else:
     return render(request,"usuarios/Login.html")
    

    
@login_required
def editar_perfil(request):
    if request.method == "POST":
        perfil = Perfil.objects.get(user=request.user)
        foto = request.POST.get("foto")
        novo_nome = request.POST.get("novo_nome")
        novo_email = request.POST.get("novo_email")

        # Atualiza foto do perfil
        if foto:
            perfil.foto = foto
            perfil.save()
        
        # Atualiza nome e email do usuário
        user = request.user
        if novo_nome and novo_nome != user.username:
            user.username = novo_nome
        if novo_email and novo_email != user.email:
            user.email = novo_email
        user.save()

        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("paginas:home")
    return render(request, "usuarios/conta.html")


@login_required
def alterar_senha(request):
    if request.method == "POST":
        user = request.user
        senha_atual = request.POST.get("current_password")
        nova_senha = request.POST.get("new_password")
        confirmar_senha = request.POST.get("confirm_password")

        if not user.check_password(senha_atual):
            messages.error(request, "Senha atual incorreta.")
            return redirect("usuarios:conta")

        if nova_senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem.")
            return redirect("usuarios:conta")

        user.set_password(nova_senha)
        user.save()
        messages.success(request, "Senha alterada com sucesso! Faça login novamente.")
        return redirect("paginas:home")  # Redireciona para o home.html da pasta paginas
    return render(request, "usuarios/conta.html")

@login_required
def excluir_conta(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Conta excluída com sucesso!")
        return redirect("paginas:home")  # Redireciona para o home.html da pasta paginas
    return render(request, "usuarios/conta.html")

   
   