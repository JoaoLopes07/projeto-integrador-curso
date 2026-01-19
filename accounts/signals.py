# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def add_user_to_afiliados_group(sender, instance, created, **kwargs):
    """
    Adiciona automaticamente novos usuários ao grupo 'afiliados'
    """
    if created:
        try:
            # Tenta obter o grupo 'afiliados'
            afiliados_group, created_group = Group.objects.get_or_create(
                name='afiliados'
            )
            
            # Adiciona o usuário ao grupo
            instance.groups.add(afiliados_group)
            
            # pode definir a role como 'afiliado' no custonuser
            if hasattr(instance, 'role'):
                # Usa update para evitar salvar novamente o usuário
                User.objects.filter(pk=instance.pk).update(role='afiliado')
                
        except Exception as e:
            # Log do erro (se necessário)
            print(f"Erro ao adicionar usuário ao grupo afiliados: {e}")