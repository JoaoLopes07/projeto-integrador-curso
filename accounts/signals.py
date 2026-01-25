from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Mapeia role (campo do usuário) → Group (Django)
ROLE_TO_GROUP = {
    "diretoria": "Diretoria",
    "associado": "Associado",
    "afiliado": "Afiliado",
    "coletivo": "Coletivo",
    "institucional": "Institucional",
}

@receiver(post_save, sender=User)
def sync_user_role_to_group(sender, instance, **kwargs):
    
    role = getattr(instance, "role", None)
    if not role:
        return

    group_name = ROLE_TO_GROUP.get(role)
    if not group_name:
        return

    
    target_group, _ = Group.objects.get_or_create(name=group_name)

    
    role_group_names = ROLE_TO_GROUP.values()
    instance.groups.remove(
        *Group.objects.filter(name__in=role_group_names)
    )

    
    instance.groups.add(target_group)
