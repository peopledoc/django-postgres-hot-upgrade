import pytest
from django.contrib.postgres import signals as postgres_signals
from django.db import connection


@pytest.fixture
def default_port(settings):
    default_port = settings.DATABASES["default"]["PORT"]
    yield
    settings.DATABASES["default"]["PORT"] = default_port
    connection.connect()


def test_integration(transactional_db, default_port, settings):
    connection.connect()
    hstore = postgres_signals.get_hstore_oids("default")
    citext = postgres_signals.get_citext_oids("default")
    pg12port = settings.PG12PORT
    # sanity check
    assert str(connection.connection.server_version).startswith("10")

    # Upgrade to Django 12
    settings.DATABASES["default"]["PORT"] = pg12port
    connection.connect()

    # Assertions
    assert str(connection.connection.server_version).startswith("12")
    assert postgres_signals.get_hstore_oids("default") != hstore
    assert postgres_signals.get_citext_oids("default") != citext
