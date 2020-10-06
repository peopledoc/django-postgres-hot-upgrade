from django.apps import AppConfig
from django.contrib.postgres import signals as postgres_signals
from django.db.backends import signals as django_signals
from django.db.backends.base.base import NO_DB_ALIAS

_version_cache = {}


def _should_run(connection):
    return connection.vendor == "postgresql" and connection.alias != NO_DB_ALIAS


def _clear():
    postgres_signals.get_hstore_oids.cache_clear()
    postgres_signals.get_citext_oids.cache_clear()


def _on_connect(connection, **kwargs):
    if not _should_run(connection=connection):
        return
    version = connection.connection.server_version
    if _version_cache.get(connection.alias) != version:
        _clear()
        _version_cache[connection.alias] = version


class PostgresHotUpgradeConfig(AppConfig):

    name = "django_postgres_hot_upgrade"

    def ready(self):
        super().ready()
        django_signals.connection_created.connect(
            _on_connect, dispatch_uid="django_postgres_hot_upgrade_dispatch_uid"
        )
