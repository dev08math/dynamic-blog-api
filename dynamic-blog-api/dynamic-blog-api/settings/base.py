from pathlib import Path
import environ

env = environ.Env()  # loading environment variables

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIR = ROOT_DIR / 'core_apps'

ROOT_URLCONF = 'dynamic-blog-api.urls'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_countries',
    'drf_yasg',
    'corsheaders',
    'phonenumber_field',
]

LOCAL_APPS = ['core_apps.profiles', 'core_apps.common', 'core_apps.users']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_preprocessors.il8n',
                'django.template.context_preprocessors.static',
                'django.template.context_preprocessors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dynamic-blog-api.wsgi.application'

# Database

DATABASES = {'default': env.db('DATABASE_URL')}

DATABASES['default']['ATOMIC_REQUESTS'] = True

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1

ADMIN_URL = env.str('ADMIN_URL', default='admin/')

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

STATIC_FILES_DIRS = []

STATICFILES_FINDER = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'mediafiles/'

MEDIA_ROOT = BASE_DIR / 'media_assets'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_URLS_REGEX = r"^/api/.*$"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format":
            "%(levelname)s %(name)-12s %(asctime)s %(module)s"
            " %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    },
}
