from django.db import models

from companies.models import Company

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('active', 'Ativo'),
        ('finished', 'finalizado'), 
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        default='pending'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name