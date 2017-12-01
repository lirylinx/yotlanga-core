from django import forms
from django.forms import ModelForm, TextInput, DateInput, PasswordInput, CheckboxInput, SelectDateWidget, EmailField, EmailInput
from yotlanga.models import Usuario, AudioTag
from django.utils.translation import ugettext_lazy as _
from . models import Ficheiro

class RegistoForm(ModelForm):
    """Registo forms."""

    class Meta:
        """Meta."""

        model = Usuario
        fields = ['nome', 'apelido', 'username', 'email', 'senha', 'numero']
        widget = {
            "nome": TextInput(attrs={}),
            "apelido": TextInput(attrs={}),
            "username": TextInput(attrs={}),
            "email":  EmailInput(attrs={}),
            "senha": PasswordInput(),
            "numero": TextInput(),
        }

        help_texts = {
            'nome': _('Escreva o teu nome')
        }

        error_messages = {
            'nome': {
                'max_length': _('Nome muito longo.')
            },
        }


class LoginForm(forms.Form):
    username_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'senha'}))


class uploadForm(forms.Form):
    descricao = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'descricao'}))
    ficheiro = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'multiple': True }))

