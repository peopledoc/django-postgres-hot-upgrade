from django.contrib.postgres import signals as postgres_signals
from django.db import connection


def test_integration(transactional_db, settings):
    connection.connect()
    hstore = postgres_signals.get_hstore_oids("default")
    citext = postgres_signals.get_citext_oids("default")
    defaultport = settings.DATABASES["default"]["PORT"]
    pg12port = settings.DATABASES["pg12"]["PORT"]
    # sanity check
    assert str(connection.connection.server_version).startswith("10")

    # Upgrade to Django 12
    settings.DATABASES["default"]["PORT"] = pg12port
    connection.connect()

    # Assertions
    try:
        assert str(connection.connection.server_version).startswith("12")
        assert postgres_signals.get_hstore_oids("default") != hstore
        assert postgres_signals.get_citext_oids("default") != citext
    finally:
        settings.DATABASES["default"]["PORT"] = defaultport
        connection.connect()
