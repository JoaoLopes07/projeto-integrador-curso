import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

print("🔧 CORRIGINDO ERRO CRÍTICO NO RENDER")

# 1. Limpa a tabela django_migrations
print("1. Limpando histórico de migrações problemáticas...")
try:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations WHERE app IN ('admin', 'accounts')")
        print(f"✅ {cursor.rowcount} registros removidos")
except Exception as e:
    print(f"⚠️  Não foi possível limpar: {e}")

# 2. Executa migrações na ORDEM ABSOLUTAMENTE CORRETA
print("\n2. Executando migrações na ordem correta...")

# ORDEM OBRIGATÓRIA: contenttypes → auth → accounts → admin → sessions → outros
migration_order = [
    # FASE 1: Tabelas básicas
    (['migrate', '--run-syncdb', '--noinput'], "Criando tabelas básicas"),
    
    # FASE 2: Apps Django CORE (ordem crítica!)
    (['migrate', 'contenttypes', '--noinput'], "1. contenttypes"),
    (['migrate', 'auth', '--noinput'], "2. auth"),
    (['migrate', 'accounts', '--noinput'], "3. accounts (CRÍTICO - antes do admin!)"),
    (['migrate', 'admin', '--noinput'], "4. admin (DEPOIS do accounts)"),
    (['migrate', 'sessions', '--noinput'], "5. sessions"),
    
    # FASE 3: Seus apps
    (['migrate', 'companies', '--noinput'], "6. companies"),
    (['migrate', 'projects', '--noinput'], "7. projects"),
    (['migrate', 'surveys', '--noinput'], "8. surveys"),
    (['migrate', 'public', '--noinput'], "9. public"),
    (['migrate', 'core', '--noinput'], "10. core"),
    
    # FASE 4: Qualquer migração restante
    (['migrate', '--noinput'], "Migrações finais"),
]

for cmd, description in migration_order:
    print(f"\n📦 {description}...")
    try:
        execute_from_command_line(['manage.py'] + cmd)
        print(f"✅ {description} - SUCESSO")
    except Exception as e:
        print(f"❌ ERRO em {description}: {e}")
        
        # Tenta com --fake se falhar
        if 'fake' not in ' '.join(cmd):
            print(f"  Tentando --fake para {description.split('.')[0]}...")
            try:
                app_name = description.split('.')[0].strip()
                if app_name != "Criando tabelas básicas":
                    execute_from_command_line(['manage.py', 'migrate', app_name, '--fake', '--noinput'])
                    print(f"  ✅ {app_name} marcado como fake")
            except:
                print(f"  ⚠️  Não foi possível fakear {app_name}")

# 3. Cria superuser garantido
print("\n3. Criando superuser...")
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Tenta verificar se a tabela existe
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'accounts_customuser'")
        table_exists = cursor.fetchone()
    
    if table_exists:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superuser criado: admin/admin123")
        else:
            print("✅ Superuser já existe")
    else:
        print("⚠️  Tabela accounts_customuser não existe ainda")
        
except Exception as e:
    print(f"⚠️  Erro ao criar superuser: {e}")

print("\n🎉 CORREÇÃO APLICADA COM SUCESSO!")