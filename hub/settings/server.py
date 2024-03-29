"""
HEROKU specific settings
"""
from .base import *   # pylint: disable=W0614,W0401
import os
import dj_database_url

ALLOWED_HOSTS = ('*',)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SSLIFY_DISABLE = os.environ.get('SSLIFY_DISABLE', False)

SECRET_KEY = os.environ.get('SECRET_KEY', None)

DEBUG = os.environ.get('DEBUG', False)  # Set env var to 1

ADMINS = (
    ('Benjamin Stookey', 'ben@aashe.org'),
)
MANAGERS = ADMINS

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('HUB_DB_URL')),
}

# Haystack ElasticSearch
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ.get('SEARCHBOX_SSL_URL', None),
        'INDEX_NAME': 'haystack',
        'TIMEOUT': 60 * 5
    },
}

# ==============================================================================
# django_membersuite_auth
# ==============================================================================
MS_ACCESS_KEY = os.environ['MS_ACCESS_KEY']
MS_SECRET_KEY = os.environ['MS_SECRET_KEY']
MS_ASSOCIATION_ID = os.environ['MS_ASSOCIATION_ID']

# ==============================================================================
# iss
# ==============================================================================
SALESFORCE_USERNAME = os.environ.get('SALESFORCE_USERNAME', None)
SALESFORCE_PASSWORD = os.environ.get('SALESFORCE_PASSWORD', None)
SALESFORCE_SECURITY_TOKEN = os.environ.get('SALESFORCE_SECURITY_TOKEN', None)

# ==============================================================================
# S3 Media Storage
# ==============================================================================

USE_S3 = os.environ.get('USE_S3', None)  # Support local dev with this config
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
WHITENOISE_IGNORE_MISSING_FILES = False

if USE_S3:
    from integration_settings.media.s3 import *
    INSTALLED_APPS += ('s3_folder_storage',)

    STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
    AWS_S3_SECURE_URLS = False
else:
    MEDIA_URL = "/media/"
    STATIC_URL = "/static/"
    MEDIA_ROOT = os.environ.get("MEDIA_ROOT", None)
    STATIC_ROOT = 'staticfiles'

# ==============================================================================
# Sentry Error Logging
# ==============================================================================

raven_dsn = os.environ.get('RAVEN_DSN', None)
if raven_dsn:
    from integration_settings.logging.sentry import *
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

# ==============================================================================
# Enable debug logging
# ==============================================================================
# LOGGING['loggers']['hub']['level'] = 'DEBUG'
# LOGGING['loggers']['django']['level'] = 'DEBUG'

# Very custom url and wsgi settings
# ROOT_URLCONF = 'hub.urls.local'
# WSGI_APPLICATION = 'hub.wsgi.local.application'
