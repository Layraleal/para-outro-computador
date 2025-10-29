from django.views.generic import TemplateView
from django.http import HttpResponse
from composteira import *
from usuarios import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    template_name = "home.html"
    
class SobreNosView(TemplateView):
    template_name = "sobrenos.html"

class MateriaisCaixaView(TemplateView):
    template_name = "materiaisCaixa.html"

class MateriaisTerraView(TemplateView):
    template_name = "materiaisTerra.html"

class TutorialCaixaView(TemplateView):
    template_name= "tutorialCaixa.html"

class TutorialTerraView(TemplateView):
    template_name = "tutorialTerra.html"

class TutorialCaixa2View(TemplateView):
    template_name = "tutorialCaixa2.html"

class TutorialCaixa3View(TemplateView):
    template_name = "tutorialCaixa3.html"      

class MateriaisCaixaM(TemplateView):
    template_name = "materiaisCaixaM.html"  



@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user, seen=False).order_by('-created_at')
    return render(request, 'notifications/notifications.html', {'notifications': notifications})


@login_required(login_url='login')
def mark_as_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.seen = True
    notif.save()
    return redirect("paginas:notifications")


@login_required(login_url='login')
def delete_notification(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.delete()
    return redirect("paginas:notifications")

@login_required
def notificacoes_registro(request):
    notifications = Notification.objects.filter(user=request.user, seen=True).order_by('-created_at')
    return render(request, 'notifications/registro.html', {'notifications': notifications})

@login_required
def mark_as_unread(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.seen = False
    notif.save()
    return redirect(request.META.get('HTTP_REFERER', 'paginas:registro_notificacoes'))



