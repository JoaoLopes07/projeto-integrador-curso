from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('diretoria', 'Diretoria'),
        ('associado', 'Associado'),
        ('afiliado', 'Afiliado'),
        ('coletivo', 'Coletivo'), 
    ]
    
    email = models.EmailField(unique=True)  # funcionalidade de email único
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='afiliado'
    )
    
    REQUIRED_FIELDS = ['email']  # obrigatorio para criação via createsuperuser
    
    def __str__(self):
        return self.email or self.username