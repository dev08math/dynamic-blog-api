import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'dynamic-blog.settings.local')

application = get_wsgi_application()
