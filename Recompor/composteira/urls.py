from django.urls import path
from .views import *
from . import views
app_name = "composteira"

urlpatterns = [
    #Urls com os views direcionados para suas respectivas funções
    path("adicionarComposteira/", views.viewAdicionarComposteira, name = "addComposteira"),
    path("adicionarCompostagem/", views.viewAdicionarCompostagem, name = "addCompostagem"),
    path("graficoGeral/", views.viewGraficoGeral, name="graficoGeral"),
    path("graficoIndividual/", views.GraficoIndividualView, name="graficoIndividual"),
    path("emissao/", views.Emissao, name='Emissao'),
    path('editarComposteira/<int:id_composteira>/', views.vieweditarComposteira, name='editarComposteira'),
    path('excluirComposteira/<int:id_composteira>/', views.viewexcluirComposteira, name='excluirComposteira'),
]