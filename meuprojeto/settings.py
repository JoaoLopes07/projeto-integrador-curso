from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do arquivo .env
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "chave-insegura-fallback")

# DEBUG - IMPORTANTE: No Render, deixe False, mas para debug temporário pode ser True
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# O Render define a variável RENDER_EXTERNAL_HOSTNAME automaticamente
render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

# ======================
# SEGURANÇA PARA RENDER (CRÍTICO!)
# ======================

if os.environ.get('RENDER'):
    # Força HTTPS no Render
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # CSRF trusted origins para o Render
    CSRF_TRUSTED_ORIGINS = [
        f'https://{render_host}',
        'https://*.onrender.com',
    ]
    
    # Logging detalhado para debug
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',

    'accounts',
    'companies',
    'projects',
    'surveys',
    'public',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meuprojeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meuprojeto.wsgi.application'

# ======================
# BANCO DE DADOS
# ======================

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {'default': DATABASE_URL.config(
        default='postgresql://postgress:ufmxwz4YEauzGSsvf8B4bmlrgkwGKIyL@dpg-d5f622juibrs7395caag-a/django_postgres_ul7a',
        conn_max_age=600,
        ssl_require=True  
        )
            }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ======================
# STATIC FILES (CRÍTICO!)
# ======================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / 'static']

# Configuração do Whitenoise para produção

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# AUTENTICAÇÃO
# ======================

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/redirect/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Sessions config (IMPORTANTE para login)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 semanas
SESSION_SAVE_EVERY_REQUEST = True

# ======================
# CRISPY FORMS
# ======================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ======================
# MIGRAÇÕES NO RENDER
# ======================

if os.environ.get('RENDER'):
    # Desativa verificação de migração problemática
    class DisableMigrationChecks:
        def __contains__(self, item):
            return True
        
        def __getitem__(self, item):
            return None
    
    MIGRATION_MODULES = DisableMigrationChecks()
    
    # Ordem forçada de migrações para evitar erro 500
    MIGRATION_MODULES = {
        'admin': None,
        'auth': None,
        'contenttypes': None,
        'sessions': None,
    }