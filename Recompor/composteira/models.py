from django.db import models
from django.contrib.auth.models import User 
#from django.contrib.auth.models import User (User, verbose_name =  "usuário", on_delete = models.CASCADE)
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


#Aqui estão as tabelas composteiras e compostagens 

class Composteira(models.Model):
    id_composteira = models.BigAutoField(primary_key = True)
    fkUsuario = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    # com_minhoca = models.BooleanField(default=False, verbose_name="Com minhoca")
    REGIAO_CHOICE = (
        ("Norte","Norte"),
        ("Nordeste", "Nordeste"),
        ("Sul", "Sul"),
        ("Sudeste","Sudeste"),
        ("Centro-Oeste", "Centro-Oeste"),
    )
    regiao = models.CharField(max_length = 12, null = False, choices = REGIAO_CHOICE)
    
    #tamanho não se mostra ser útil no cálculo

    TIPO_CHOICE = (

        ("Terra", "Terra"),
        ("Caixa", "Caixa" ),
    )
    tipo = models.CharField(max_length = 5, null = False, choices = TIPO_CHOICE)

    data_construcao = models.DateField(verbose_name="Data construção")
    nome = models.CharField(max_length = 50)
    
    imagem = models.ImageField(
        upload_to='composteiras/', 
        blank=True, 
        null=True,
        verbose_name="Imagem da composteira"
    )


class Compostagem(models.Model):
    id_compostagem = models.BigAutoField(primary_key = True)
    fkComposteira = models.ForeignKey(Composteira, verbose_name =  "composteira", on_delete = models.CASCADE)
    fkUsuario_comp = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    data_inicio = models.DateField(verbose_name="Data colocado")
    data_pronto = models.DateField(null=True, blank=True)
    peso = models.FloatField()
  
       #função responsável por calcular em quantos dias a compostagem estará pronta     
    def calcular(self):
        regiao_m = {
            'Norte': 0.90,
            'Nordeste': 0.95,
            'Centro-Oeste': 0.95,
            'Sudeste': 1.00,
            'Sul': 1.20
        }
        composteira = self.fkComposteira
        # define clima
        clima = "quente" if composteira.regiao in (
            'Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste'
        ) else 'frio'

        # base de dias pelo tipo da composteira
        if composteira.tipo.lower() == "caixa":
            base_days = 30 if clima == "quente" else 45
        else:  # terra
            base_days = 60 if clima == "quente" else 120

        # fator pelo peso (ex: +1% no tempo a cada 1kg)
        try:
            peso = float(self.peso)
        except (TypeError, ValueError):
            peso = 0  # se não tiver peso válido, não altera

        fator_peso = 1 + (peso / 100)

        # cálculo final
        dias = round(base_days * regiao_m[composteira.regiao] * fator_peso)
        data_pronta = self.data_inicio + timedelta(days=dias)

        return dias, data_pronta
    
    def save(self, *args, **kwargs):
    # sempre calcula antes de salvar
        if self.data_inicio and self.fkComposteira:
            dias, data_prevista = self.calcular()
            self.data_pronto = data_prevista
        super().save(*args, **kwargs)