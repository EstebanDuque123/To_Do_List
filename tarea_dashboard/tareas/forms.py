from django import forms
from .models import Tarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'categoria']



class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
