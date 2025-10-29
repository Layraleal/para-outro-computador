from django.db import models
from django.contrib.auth.models import User

# 1. Definindo as opções de fotos
FOTOS_CHOICES = [
    ("foto1.png", "Foto 1"),
    ("foto2.png", "Foto 2"),
    ("foto3.png", "Foto 3"),
]

# 2. Modelo Perfil
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.CharField(max_length=50, choices=FOTOS_CHOICES, default="foto1.png")

    def __str__(self):
        return self.user.username

# 3. Sinal: cria automaticamente o Perfil após o User ser criado
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
