from django.contrib import admin

# Register your models here.
from .models import Composteira, Compostagem


#Os registros que estão salvos no adm 

admin.site.register(Composteira)
admin.site.register(Compostagem)