from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Cria grupos e permissões do projeto (versão final)."

    def handle(self, *args, **options):
        # 1) Pegar ContentType global (usado para permissões não atreladas a um modelo específico)
        ct_global = ContentType.objects.get_for_model(Group)

        # 2) Criar permissões extras (globais / por domínio)
        perms_to_create = [
            # Acesso e gestão
            ("manage_access", "Pode gerenciar permissões e acessos (Diretoria)"),

            # Companies
            ("change_any_company", "Pode editar qualquer empresa (Diretoria)"),
            ("change_own_company", "Pode editar apenas suas empresas (Associado)"),

            # Reports / Public
            ("view_aggregated_reports", "Pode ver relatórios agregados"),
            ("view_public_map", "Pode acessar mapa público"),
        ]

        created = 0
        for codename, name in perms_to_create:
            perm, was_created = Permission.objects.get_or_create(
                codename=codename,
                content_type=ct_global,
                defaults={"name": name},
            )
            created += int(was_created)

        # 3) Grupos
        g_diretoria, _ = Group.objects.get_or_create(name="Diretoria")
        g_associado, _ = Group.objects.get_or_create(name="Associado")
        g_afiliado, _ = Group.objects.get_or_create(name="Afiliado")
        g_coletivo, _ = Group.objects.get_or_create(name="Coletivo/Institucional")

        # 4) Pegar as permissões criadas
        def p(code: str) -> Permission:
            return Permission.objects.get(codename=code, content_type=ct_global)

        # 5) Atribuir permissões por grupo
        # Diretoria: acesso total + gerenciar acessos
        g_diretoria.permissions.add(
            p("manage_access"),
            p("change_any_company"),
            p("view_aggregated_reports"),
            p("view_public_map"),
        )

        # Associado: editar “suas” empresas + projetos + preencher pesquisa
        g_associado.permissions.add(
            p("change_own_company"),
            p("view_public_map"),
        )

        # Afiliado: editar perfil + preencher pesquisa
        g_afiliado.permissions.add(
            p("view_public_map"),
        )

        # Coletivo/Institucional: acesso a busca/análise/filtros públicos + relatórios agregados (limitado)
        g_coletivo.permissions.add(
            p("view_public_map"),
            p("view_aggregated_reports"),
        )

        self.stdout.write(self.style.SUCCESS(
            f"OK: permissões extras criadas: {created}. Grupos e permissões configurados."
        ))