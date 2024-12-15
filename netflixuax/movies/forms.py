from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }


class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nuevo nombre de usuario'}),
        }

class UserGenresForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Suponiendo que tienes un modelo UserProfile relacionado
        fields = ['favorite_genres']
        widgets = {
            'favorite_genres': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        }
