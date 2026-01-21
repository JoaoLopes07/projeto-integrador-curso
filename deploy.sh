# build.sh
#!/usr/bin/env bash

set -o errexit

# Instalar dependências
pip install -r requirements.txt

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Aplicar migrações
python manage.py migrate --run-syncdb  # Esta opção pode ajudar

# Ou se preferir forçar
python manage.py migrate auth
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate sessions
python manage.py migrate accounts