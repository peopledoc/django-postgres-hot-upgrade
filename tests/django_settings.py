import os

DEBUG = True

SECRET_KEY = "secret-key"

INSTALLED_APPS = [
    "django_postgres_hot_upgrade",
    "django.contrib.postgres",
    "tests",
]


def _db(default_port):
    return


PG12PORT = os.environ.get("PG12PORT", "5433")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # All other connection params are read from environment
        # https://www.postgresql.org/docs/current/libpq-envars.html
        "NAME": os.environ["PGDATABASE"],
        "TEST": {
            "NAME": os.environ["PGDATABASE"],
        },
    },
}
