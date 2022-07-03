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
    'djcelery_email',
    'djoser',
    'rest_framework_simplejwt',
]

LOCAL_APPS = ['core_apps.profiles', 'core_apps.common', 'core_apps.users', 'core_apps.favorites', 'core_apps.articles', 'core_apps.ratings', 'core_apps.comments', 'core_apps.reactions']

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
        'DIRS': [APPS_DIR / 'templates'],
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

WSGI_APPLICATION = 'dynamic-blog-api.wsgi.application'

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

ADMIN_URL = 'admin/'

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'staticfiles/'

STATIC_FILES_DIRS = []

STATICFILES_FINDER = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_ROOT = ROOT_DIR / 'staticfiles'

MEDIA_URL = 'mediafiles/'

MEDIA_ROOT = ROOT_DIR / 'mediafiles'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_URLS_REGEX = r"^/api/.*$"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER" : "core_apps.common.exceptions.custom_exception_handler",
    "NON_FIELD_ERRORS_KEY" : "error",
    "DEFAULT_AUTHENTICATION_CLASSES":(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {              # for generation of tokens
    "AUTH_HEADER_TYPES":(
        'Bearer',
        'JWT',
    ),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),    # user will have to login every day
    "SIGNING_KEY" : env("SIGNING_KEY"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_TOKEN_CLASSES" : ("rest_framework_simplejwt.tokens.AccessToken",), 
}

DJOSER = {      
    # has to do nothing with 'generation' of tokens. Its all about the user management and authentication
    # uses jwt in its backend for generation of tokens, can also user normal token base authentication
    # proper endpoints for managing user registration, management and authenticatiion is given in the docs

    'LOGIN_FIELD' : 'email',
    'USER_CREATE_PASSWORD_RETYPE' : True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION' : True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION' : True,
    # 'SEND_CONFIRMATION_EMAIL' : True,

    # URL are used for frontend and given to it.
    # the 'uid' and 'token' for example are the input to given in JSON format in the request.
    # inorder to give the proper endpoints for the respective functionality, refer the base endpoints docs of djoser 
    # remember that proper endpoints for the functionalities are in stated in the docs, the URLs below are strictly for the frontend
    'PASSWORD_RESET_CONFIRM_URL' : 'password/reset/confirm/{uid}/{token}',
    'SET_PASSWORD_RETYPE' : True,    # functionality for asking the user to retype the resetted/new password
    'PASSWORD_RESET_CONFRIM_RETYPE' : True, # functionality for asking the user to confirm to the new resetted password
    'USERNAME_RESET_CONFIRM_URL' : 'email/reset/confrim/{uid}/{token}',
    # 'ACTIVATION_URL' : 'activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL' : True,

    # for knowing more about the keys of the 'SERIALIZERS' refer the docs
    'SERIALIZERS' : {  
        'user_create' : 'core_apps.users.serializers.UserCreateSerializer',  # using the overrided serializer of djoser
        'user' : 'core_apps.users.serializers.UserSerializer',
        'current_user' : 'core_apps.users.serializers.UserSerializer',
        'user_delete' : 'djoser.serializers.UserDeleteSerializer',
    }
}
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

CELERY_BROKER_URL = env('CELERY_BROKER')

CELERY_RESULT_BACKEND = env('CELERY_BACKEND')

CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'pickle']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'