import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'na2p&yexkp-g83$2m^&b!r+a%nv2ci1!d9vh^a_7h!hv*7&h79'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'stressboard',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'stressboard.urls'

WSGI_APPLICATION = 'stressboard.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

LOADS_DATABASE = {
    'backend': 'redis',
    'options': {
    }
}

LOADS_BROKER = 'ipc:///tmp/loads-front.ipc'
