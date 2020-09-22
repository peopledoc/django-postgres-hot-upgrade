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
        "django_postgres_hot_upgrade",
        "django.contrib.postgres",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            # All other connection params are read from environment
            # https://www.postgresql.org/docs/current/libpq-envars.html
            "NAME": os.environ["PGDATABASE"],
        }
    },
)


def index(request):
    connection.connect()
    version = connection.connection.server_version
    return HttpResponse(f"<h1>You're using pg {version}</h1>")


urlpatterns = [
    url(r"^$", index),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
