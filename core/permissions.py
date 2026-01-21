def in_group(user, name: str) -> bool:
    return bool(
        user
        and user.is_authenticated
        and user.groups.filter(name=name).exists()
    )


def is_diretoria(user) -> bool:
    if not (user and user.is_authenticated):
        return False

    return (
        user.has_perm("auth.manage_access")
        or user.has_perm("auth.change_any_company")
    )


def is_associado(user) -> bool:
    return in_group(user, "Associado")


def is_afiliado(user) -> bool:
    return in_group(user, "Afiliado")


def is_coletivo(user) -> bool:
    return in_group(user, "Coletivo")


# =========================
# PERMISSÕES DE NEGÓCIO
# =========================

def can_manage_companies(user) -> bool:
    return is_diretoria(user)


def can_manage_projects(user) -> bool:
    return is_diretoria(user)


def can_access_projects_area(user) -> bool:
    return is_diretoria(user) or is_associado(user)


def can_edit_own_profile(user) -> bool:
    """
    Todo usuário autenticado pode editar seu próprio perfil
    """
    return bool(user and user.is_authenticated)


def can_view_company_data(user) -> bool:
    """
    Diretoria vê qualquer empresa
    Associado vê apenas a própria (controlado na view)
    """
    return is_diretoria(user) or is_associado(user)
