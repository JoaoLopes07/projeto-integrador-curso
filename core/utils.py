from .models import AuditLog


def log_action(user, action, model_name, object_id=None, description=""):
    AuditLog.objects.create(
        user=user if user.is_authenticated else None,
        action=action,
        model_name=model_name,
        object_id=str(object_id) if object_id else "",
        description=description
    )
