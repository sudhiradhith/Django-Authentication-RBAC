"""
Django settings for myproject project.

Lab - 3B: User Authentication & Role-Based Access Control (RBAC)
Course: Full Stack Web Development (MDSO508-3)
"""

from pathlib import Path

# BASE_DIR points to the lab3b project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lab3b-rbac-auth-key-super-secret-demo-change-in-prod'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver', '*']


# Application definition: List of active apps
INSTALLED_APPS = [
    'django.contrib.admin',         # Built-in admin interface
    'django.contrib.auth',          # Authentication framework (Users, Groups, Permissions)
    'django.contrib.contenttypes',  # Content types system
    'django.contrib.sessions',      # User sessions
    'django.contrib.messages',      # Flash messaging
    'django.contrib.staticfiles',   # Static assets
    'accounts.apps.AccountsConfig', # Accounts application with RBAC & Auth logic
]

# Global request / response processing middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_role_context', # Custom role context for templates
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database Configuration
# Uses default SQLite database located at lab3b/db.sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation rules enforced during registration & password reset
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication Redirections
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Task 2: Password Reset Email Backend
# In development, console backend prints reset links/tokens directly to the server terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@lab3b.university.edu'
