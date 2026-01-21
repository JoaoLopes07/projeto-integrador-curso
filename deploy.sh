

echo "🚀 Iniciando deploy..."

# Instala dependências
pip install -r requirements.txt

# Coleta estáticos
python manage.py collectstatic --noinput

# Verifica se o módulo wsgi existe
echo "🔍 Verificando estrutura do projeto..."
if [ -f "meuprojeto/wsgi.py" ]; then
    echo "✅ meuprojeto/wsgi.py encontrado"
else
    echo "❌ meuprojeto/wsgi.py não encontrado"
    echo "Estrutura atual:"
    find . -name "*.py" -type f | grep -E "(wsgi|settings)\.py$"
    exit 1
fi

# Executa migrações
python manage.py migrate --noinput

echo "✅ Build concluído!"