import os
import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.db import connection
from django.http import HttpResponse

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=sys.modules[__name__],
    INSTALLED_APPS=[
        'postgres_hot_update',
        'django.contrib.postgres',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("PGDATABASE"),
            'USER': os.getenv("PGUSER"),
            'PASSWORD': os.getenv("PGPASSWORD"),
            'HOST': os.getenv("PGHOST"),
            'PORT': os.getenv("PORT"),
        }
    }
)


def index(request):
    with connection.cursor() as cursor:
        version = connection.connection.server_version
    return HttpResponse(f"<h1>You're using pg {version}</h1>")

urlpatterns = [
    url(r'^$', index),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
