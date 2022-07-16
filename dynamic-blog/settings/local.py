
from .base import *
from .base import env

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default='django-insecure-peocn)7g4q-jg-ic23lzx*%2o74zj6_@1itp+^33ns9dpbplcc'
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

ADMINS = [("""Django Admin""", "api.djangoadmin@dynamicblog.com")]

MANAGERS = ADMINS

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

EMAIL_HOST = env('EMAIL_HOST', default='mailhog')

EMAIL_PORT = env('EMAIL_PORT')

DEFAULT_FROM_EMAIL = 'info@blog-api.com'

DOMAIN = env('DOMAIN')

SITE_NAME = 'Dynamic Blog API'
