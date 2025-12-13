from django.contrib.admin import AdminSite

class AdminSite(AdminSite):
    site_header = 'Meu Sistema Administrativo'
    site_title = 'Painel de Controle'
    index_title = 'Bem-vindo ao Painel de Controle'
    
admin_site = AdminSite(name='admin')