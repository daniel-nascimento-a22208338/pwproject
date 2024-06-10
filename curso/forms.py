# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Curso
from .models import Disciplina
from .models import Projeto

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'  # Adicionar todos os campos
        widgets = {
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição do Projeto'}),
            'imagem': forms.ClearableFileInput(),
        }

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'  # Altere conforme necessário
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da Disciplina'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição'}),
        }

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do Curso'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição do Curso'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }