#!/bin/bash
set -e

echo "🚀 Iniciando deploy no Render..."

# 1. Instala dependências
pip install -r requirements.txt

# 2. Encontra ou cria estrutura
if [ ! -d "meuprojeto" ]; then
    echo "⚠️  meuprojeto/ não encontrado, buscando projeto..."
    PROJECT_NAME=$(find . -name "settings.py" -type f | head -1 | xargs dirname | xargs basename)
    if [ -n "$PROJECT_NAME" ] && [ "$PROJECT_NAME" != "meuprojeto" ]; then
        echo "🔁 Renomeando $PROJECT_NAME para meuprojeto..."
        mv "$PROJECT_NAME" meuprojeto
    fi
fi

# 3. Cria wsgi.py
mkdir -p meuprojeto
cat > meuprojeto/wsgi.py << 'EOF'
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
application = get_wsgi_application()
EOF

# 4. Atualiza manage.py se necessário
sed -i "s/config\.settings/meuprojeto.settings/g" manage.py 2>/dev/null || true

# 5. Coleta estáticos
python manage.py collectstatic --noinput

# 6. Migrações
python manage.py migrate --noinput

echo "✅ Build concluído!"