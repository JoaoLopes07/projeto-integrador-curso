## 📋 Sobre o Projeto
Sistema web desenvolvido em Django com arquitetura modular, focado em autenticação de usuários e controle de acesso baseado em perfis. O projeto implementa um sistema robusto de gerenciamento com separação clara entre funcionalidades públicas, de usuários autenticados e administrativas.

## 🎯 Tecnologias Utilizadas

Python 

Django 

HTML/CSS (templates Django)

SQLite/PostgreSQL (banco de dados)

Django Authentication System

## 🚀 Sprint 1 - Autenticação e Usuários (Concluída)

## ✅ Funcionalidades Implementadas

# 1. Estrutura do Projeto

> Criação do app accounts separado do projeto principal (meuprojeto)

> Configuração de URLs modularizadas

> Separação lógica entre views de autenticação e views do app

# 2. Modelo de Usuário

> Sistema de permissões e grupos

> Diferenciação entre usuários comuns e administradores

# 3. Sistema de Autenticação

> Login personalizado (/accounts/login/)
>
> Registro de novos usuários (/accounts/register/)
>
> Logout seguro (/accounts/logout/)

> Redirecionamento automático baseado no tipo de usuário

# 4. Recuperação de Senha

> Sistema completo de reset de senha
>
> Templates personalizados para cada etapa:
>
> Solicitação de reset
>
> Confirmação de envio
>
> Formulário de nova senha
>
> Confirmação de conclusão

# 5. URLs Implementadas
> Públicas (não requerem autenticação):
> /accounts/login/ - Página de login
>
> /accounts/register/ - Registro de novos usuários
>
> /accounts/password_reset/ - Solicitar reset de senha
>
> Privadas (requerem autenticação):
> /accounts/logout/ - Encerrar sessão
>
> /accounts/home/ - Página inicial após login
>
> /accounts/profile/ - Perfil do usuário
>
> Administrativas:
> /admin/ - Painel de administração do Django
>
> URLs para gerenciamento de usuários através do admin nativo

# 6. Redirecionamentos Inteligentes

> Redirecionamento de /login/ para /accounts/login/ (permanente)
>
> Redirecionamento pós-login baseado no tipo de usuário
>
> Fluxo seguro para páginas protegidas

## 🔒 Sistema de Segurança
>   Autenticação segura usando sessões Django
>
>    Proteção contra CSRF
>
>   Views protegidas com decorators @login_required
>
>   Senhas hasheadas com algoritmos seguros
>
>  Tokens únicos para recuperação de senha

# 🎨 Templates e Interface

>Templates personalizados para autenticação
>
>Layouts responsivos
>
>Mensagens de feedback para o usuário
>
>Formulários com validação client-side e server-side

# 📁 Estrutura de URLs Principais

# URLs públicas

> path('accounts/login/', ...)      # Login
> path('accounts/register/', ...)   # Registro

# URLs protegidas

> path('accounts/logout/', ...)     # Logout
> path('accounts/home/', ...)       # Home
> path('accounts/profile/', ...)    # Perfil

# URLs administrativas

> path('admin/', ...)               # Admin Django
> (Futuro: painel admin customizado)

## 🔄 Fluxo de Autenticação

> Usuário não autenticado: Acesso apenas a login e registro

> Login bem-sucedido: Redirecionamento para /accounts/home/

> Usuário comum: Acesso a home e perfil

> Administrador: Acesso adicional ao painel /admin/

> Logout: Encerra sessão e redireciona para login

## 🛠️ Configuração e Instalação
>bash
> #Clonar repositório
>git clone [url-do-repositorio]
>
> #Instalar dependências
>pip install -r requirements.txt
>
> #Configurar banco de dados
>python manage.py migrate
>
> #Criar superusuário
>python manage.py createsuperuser
>
># Executar servidor
> python manage.py runserver
>

## 📈 Próximas Sprints (Planejadas)

## Sprint 2: 

> Criar app companies
> Criar model Company
> CRUD básico de empresas
> Criar página pública simples de empresas


## Sprint 3:

> Criar app projects
> Criar model Project
> CRUD básico de projetos

## Sprint 4:

>Criar app surveys
>Criar modelos SurveyYear e SurveyResponse
>Criar formulário de pesquisa anual
>Configuração de permissões por tipo de usuário
>Criação do layout base com Bootstrap
