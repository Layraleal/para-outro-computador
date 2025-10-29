from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Notification
from django.contrib.auth.models import User
from django.db.models.signals import post_save


@receiver(user_logged_in)
def create_login_notification(sender, request, user, **kwargs):
    # Só cria notificação de login se NÃO for o primeiro login
    if user.last_login:
        ip = get_client_ip(request)
        Notification.objects.create(
            user=user,
            message=f'<span class="notificacao-login">Novo login detectado no IP: {ip}</span>'
        )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',') if ip.strip()]
        ip = ip_list[0] if ip_list else None
    else:
        ip = request.META.get('REMOTE_ADDR')
    if not ip:
        ip = 'IP não identificado'
    return ip

@receiver(post_save, sender=User)
def welcome_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            message="""
                <div class="titulo-boas-vindas">🌱 <b>Bem-vindo(a) ao Recompor!</b> 🌱</div>
                <div>
                    Aqui acreditamos que pequenas ações do dia a dia podem transformar o mundo.<br>
                    O Recompor nasceu para ajudar você a descobrir como a compostagem doméstica pode reduzir o lixo, nutrir a terra e trazer mais sustentabilidade para sua rotina.<br><br>
                    Explore nossos conteúdos, aprenda passo a passo como começar e inspire-se a dar um novo destino aos seus resíduos orgânicos.<br>
                    <b>Juntos, vamos recompor a natureza, de dentro de casa para o planeta. 🌍💚</b>
                </div>
            """
        )