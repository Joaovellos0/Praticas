from django import forms
from django.contrib.auth.models import User
from .models import Usuario


class CadastroForm(forms.ModelForm):
    nome = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Usuario
        fields = [
            "telefone",
            "cep",
            "logradouro",
            "bairro",
            "cidade",
            "estado",
            "numero",
            "complemento",
        ]
