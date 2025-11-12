from django.urls import path
from . import views



app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.entrar, name = "entrar"),
    path("login/", views.logar, name = "logar"),
    path('deslogar/',views.deslogar,name='deslogar'),
    path("esqueceuSenha/",views.esqueceuSenha, name = "esqueceuSenha"),
    path("conta/", views.logarconta, name = "conta"),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('excluir_conta/', views.excluir_conta, name='excluir_conta'),
    path('ajax/username_available/', views.username_available, name='username_available'),
    


        
]










