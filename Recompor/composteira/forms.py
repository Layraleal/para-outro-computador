from django import forms
from .models import Composteira
from .models import Compostagem


#editar composteira


class ComposteiraForm(forms.ModelForm):
    class Meta:
        model = Composteira
        fields = ['nome', 'data_construcao', 'regiao', 'tipo', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_construcao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            #'tamanho': forms.Select(attrs={'class': 'form-control'}),
            'regiao': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }



#class CompostagemForm(forms.ModelForm):
    #class Meta:
        #model = Compostagem
        #fields = ['fkComposteira', 'data_inicio', 'peso']