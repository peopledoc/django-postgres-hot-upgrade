from django.apps import AppConfig

from django.contrib.postgres.signals import (
    get_citext_oids, get_hstore_oids
)
from django.db.backends.base.base import NO_DB_ALIAS
from django.db.backends.signals import connection_created


_version_cache = {}


def _on_connect(connection, **kwargs):
    if connection.vendor != 'postgresql' or connection.alias == NO_DB_ALIAS:
        return
    version = connection.connection.server_version
    if _version_cache.get(connection.alias) != version:
        get_hstore_oids.cache_clear()
        get_citext_oids.cache_clear()
        _version_cache[connection.alias] = version


class PostgresHotUpdateConfig(AppConfig):

    name = 'postgres_hot_update'

    def ready(self):
        super().ready()
        connection_created.connect(_on_connect)
