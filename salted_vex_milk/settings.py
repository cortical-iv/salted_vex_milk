"""
Django settings for salted_vex_milk project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import logging
from django.core.exceptions import ImproperlyConfigured



logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger.debug(f"base_dir: {BASE_DIR}")

# SECURITY WARNING: keep the secret key used in production secret!
def get_env_variable(var_name):
    """get environmental variable, or return exception
    Taken from Section 5.3.5 Two Scoops"""
    try:
        return os.environ.get(var_name)
    except KeyError:
        error_msg = 'get_env_variable error: Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env_variable('SECRET_KEY')
D2_KEY =  get_env_variable('D2_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #third-party apps
    'django_tables2',

    #my apps
    'd2api',
    'clans',
    'members',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'salted_vex_milk.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'salted_vex_milk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vexdata',
        'USER': 'eric',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


### Static files (CSS, JavaScript, Images)
### https://docs.djangoproject.com/en/1.11/howto/static-files/
#STATIC_URL = '/static/'
#
##Static asset configuration [new from https://devcenter.heroku.com/articles/django-assets]
#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
#STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')  #'staticfiles'
#STATICFILES_DIRS = (
#        os.path.join(PROJECT_ROOT, 'static'),
#        )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
logger.debug(f"BASE_DIR: {BASE_DIR}")

# Extra places for collectstatic to find static files.
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)
#logger.debug(f"STATIFILES_DIRS: {STATICFILES_DIRS}")


#Heroku settings
cwd = os.getcwd()
if cwd == '/app' or cwd[:4] == '/tmp':  #can just get rid of this: use one sent in docs

    import dj_database_url  #uses url in lieu of above if given settings usse configs sent!
    DATABASES = {
            'default': dj_database_url.config(default = 'postgres://localhost')}

    #Honor the 'X-Forwarded-Proto' header for request.is_secure().
    SECURE_PROXY_SSL_HEADER = {'HTTP_X_FORWARDED_PROTO', 'https'}  #can be on localhost

    #Allow only Heroku to host the project
    ALLOWED_HOSTS =  ['localhost', 'saltedvexmilk.herokuapp.com'] #['tell-jeeves.herokuapp.com']  #make list of valid things, not *
    DEBUG = False  #make this an environment variable (so you can set it at heroku quickly if you need it)
    #following yields 500 error at heroku
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

