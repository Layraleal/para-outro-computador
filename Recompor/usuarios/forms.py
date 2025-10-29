from django import forms
from django.contrib.auth.models import User
from accounts.models import Perfil  # ← observe o import do outro app

class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    foto = forms.ChoiceField(choices=Perfil._meta.get_field('foto').choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Perfil.objects.create(user=user, foto=self.cleaned_data['foto'])
        return user
