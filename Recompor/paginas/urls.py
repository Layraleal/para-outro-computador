from django.urls import path
from .views import *

app_name= "paginas"

urlpatterns = [
    path('', IndexView.as_view(), name="home"),
    path('sobrenos/',SobreNosView.as_view(), name="sobrenos"),
    path('tutorialCaixa/', TutorialCaixaView.as_view(), name = "tutCaixa"),
    path('tutorialTerra/', TutorialTerraView.as_view(), name = "tutTerra"),
    path('materiaisCaixa/', MateriaisCaixaView.as_view(), name = "matCaixa"),
    path('materiaisTerra/', MateriaisTerraView.as_view(), name = "matTerra"),
    path('tutorialCaixa2', TutorialCaixa2View.as_view(), name = "tutCaixa2"),
    path('tutorialCaixa3', TutorialCaixa3View.as_view(), name = "tutCaixa3"),
    path('materiaisCaixaM/', MateriaisCaixaM.as_view(), name="caixaM"),
    path('materiaisCaixaG/', MateriaisCaixaG.as_view(), name="caixaG"),
 
    path("notificacoes/", notifications_view, name="notifications"),
    path("notificacoes/marcar/<int:notif_id>/", mark_as_read, name="mark_as_read"),
    path("notificacoes/remover/<int:notif_id>/", delete_notification, name="delete_notification"),
    path('registro/', notificacoes_registro, name='registro_notificacoes'),
    path('notificacoes/<int:notif_id>/marcar_nao_lida/', mark_as_unread, name='mark_as_unread'),
    
    
]