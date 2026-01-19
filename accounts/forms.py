from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group  
from django.core.exceptions import ValidationError

# Obtém o modelo de usuário atual (CustomUser)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Formulário personalizado para criação de usuários usando CustomUser"""
    
    # Campos adicionais do CustomUser
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email (obrigatório)'
        })
    )
    
    telefone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone (opcional)'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'telefone', 'password1', 'password2')
    
    def clean_email(self):
        """Valida que o email é único"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'afiliado'  # Define role como afiliado
        
        if commit:
            user.save()
            # O signal vai cuidar de adicionar ao grupo
            # Mas podemos garantir aqui também:
            self.add_to_afiliados_group(user)
        
        return user
    
    def add_to_afiliados_group(self, user):
        """Adiciona usuário ao grupo afiliados"""
        try:
            afiliados_group, created = Group.objects.get_or_create(
                name='afiliados'
            )
            user.groups.add(afiliados_group)
        except Exception as e:
            # Em produção, use logging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao adicionar usuário ao grupo: {e}")