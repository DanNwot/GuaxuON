from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de Segurança (Desenvolvimento)
SECRET_KEY = 'django-insecure-uwwhfgff+q)6()d5+@a5m-5s9@h*66q*624wgkp_#q6ri=$c0^'
DEBUG = True
ALLOWED_HOSTS = []

# Definição de Aplicativos
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app', # Seu aplicativo principal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # CERTIFIQUE-SE DE QUE A LINHA ABAIXO ESTÁ EXATAMENTE ASSIM:
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Banco de Dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'GuaxuON',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Validação de Senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localização e Fuso Horário (Brasil)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS (CSS, JS, IMAGENS) ---
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'app' / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURAÇÕES DO SISTEMA DE LOGIN / LOGOUT ---
# Onde o usuário cai após logar com sucesso (Página Inicial)
LOGIN_REDIRECT_URL = '/'  

# Onde o usuário cai após fazer logout (Redireciona para a tela de Login usando o nome da rota)
LOGOUT_REDIRECT_URL = 'login'

# Rota para onde o Django barra usuários não logados que tentam acessar páginas restritas
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'