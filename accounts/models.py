from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)  # funcionalidade de email único
    
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
    # propriedades para compatibilidade
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # obrigatorio para criação via createsuperuser
    
    def __str__(self):
        return self.email or self.username