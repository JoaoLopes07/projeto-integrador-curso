## 📋 Sobre o Projeto

Sistema web desenvolvido em **Django**, com arquitetura modular por aplicativos (apps), focado em **autenticação**, **gestão de empresas**, **projetos**, **pesquisas (surveys)** e **informações de acesso públiuco (public)**.

Este repositório representa o **projeto oficial do grupo**, com decisões arquiteturais já consolidadas e evolução contínua do código.

---

## 🎯 Objetivo do Projeto

O projeto tem como objetivo aplicar, de forma prática:

- Organização de projetos Django em equipe
- Boas práticas de versionamento com Git/GitHub
- Separação clara de responsabilidades por app
- Controle de acesso e permissões
- Padronização de templates, URLs e estrutura do projeto

---

## 🧩 Apps do Projeto
```
accounts/ → autenticação, login, cadastro e perfil de usuário
companies/ → gestão de empresas e representantes
projects/ → gestão de projetos vinculados a empresas
surveys/ → pesquisas e formulários
templates/ → templates HTML centralizados
static/ → arquivos estáticos (CSS)
```
---

## 🛠️ Tecnologias Utilizadas

- Python
- Django
- HTML / CSS (templates Django)
- SQLite (desenvolvimento)
- Git e GitHub (versionamento em equipe)

---

## 🚀 Como rodar o projeto localmente

### 1. Clonar o repositório


**git clone** https://github.com/JoaoLopes07/projeto-integrador-curso.git

**cd** projeto-integrador-curso

### 2. Criar e ativar ambiente virtual

 **Windows**

- python -m venv venv
- venv\Scripts\activate

**Linux / macOS**

- python -m venv venv
- source venv/bin/activate

### 3. Instalar dependências

- pip install -r requirements.txt

### 4. Aplicar migrações e criar superusuário

- python manage.py migrate
- python manage.py createsuperuser

### 5. Rodar o servidor

- python manage.py runserver

### Acesse no navegador:

- http://localhost:8000/


## 📐 Padrões e Decisões do Projeto

Esta seção documenta decisões técnicas já fechadas pela equipe, para manter consistência no desenvolvimento.

📁 Templates
Todos os templates ficam centralizados na pasta raiz templates/

Os apps não possuem pasta de templates própria

Uso de:

- base.html como template base

- {% include %} para componentes reutilizáveis

- {% block %} para extensões de layout

### 🌐 URLs

- Cada app possui seu próprio `urls.py`
- As URLs são organizadas por **namespace (`app_name`)**
- Prefixos definidos:
  - `/` → public (páginas públicas / landing)
  - `accounts/` → autenticação
  - `companies/` → empresas
  - `projects/` → projetos
  - `pesquisa/` → surveys



### 🧠 Views e Permissões

Uso de Class Based Views (CBVs) sempre que possível

Proteção de views com:

- @login_required

- validações manuais de permissão quando necessário

- Usuários da diretoria/admin possuem permissões amplas

- Usuários representantes têm acesso restrito aos dados da sua empresa

### 🏢 Relação Usuário ↔ Empresa

- Um usuário pode estar vinculado a uma empresa 

- Diretoria/admin não depende de vínculo com empresa

- Lógicas de acesso sempre consideram a possibilidade de:

- company ser None

- representante ser None

**(Esses casos devem ser tratados para evitar erros e exibir mensagens amigáveis.)**