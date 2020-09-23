import pytest
from django.db.backends import signals as django_signals

from django_postgres_hot_upgrade import app


@pytest.fixture(autouse=True)
def module_cache():
    app._version_cache = {}
    yield
    app._version_cache = {}


@pytest.mark.parametrize(
    "vendor, alias, expected",
    [
        ("mysql", "default", False),
        ("postgresql", "__no_db__", False),
        ("postgresql", "default", True),
    ],
)
def test_should_run(mocker, vendor, alias, expected):
    connection = mocker.Mock(vendor=vendor, alias=alias)
    assert app._should_run(connection) is expected


def test_config_ready():
    # receivers look like:
    # [(('django_postgres_hot_upgrade_dispatch_uid', 9447968), <weakref>),
    #  ((140367743599664, 9447968), <weakref>)]
    assert "django_postgres_hot_upgrade_dispatch_uid" in {
        r[0][0] for r in django_signals.connection_created.receivers
    }


@pytest.fixture
def fake_connection(mocker):
    return mocker.Mock(vendor="postgresql", alias="default")


def test_on_connect_should_not_run(fake_connection, mocker):
    clear = mocker.patch("django_postgres_hot_upgrade.app._clear")
    fake_connection = mocker.Mock(vendor="mysql", alias="default")
    app._on_connect(connection=fake_connection)
    clear.assert_not_called()


def test_on_connect_first_call(fake_connection, mocker):
    clear = mocker.patch("django_postgres_hot_upgrade.app._clear")
    fake_connection.connection.server_version = 100000
    app._on_connect(connection=fake_connection)
    assert app._version_cache == {"default": 100000}
    clear.assert_called()


def test_on_connect_second_call_same_version(fake_connection, mocker):
    clear = mocker.patch("django_postgres_hot_upgrade.app._clear")
    fake_connection.connection.server_version = 100000
    app._on_connect(connection=fake_connection)
    clear.reset_mock()
    app._on_connect(connection=fake_connection)
    clear.assert_not_called()


def test_on_connect_second_call_different_version(fake_connection, mocker):
    clear = mocker.patch("django_postgres_hot_upgrade.app._clear")
    fake_connection.connection.server_version = 100000
    app._on_connect(connection=fake_connection)
    fake_connection.connection.server_version = 120000
    clear.reset_mock()
    app._on_connect(connection=fake_connection)
    assert app._version_cache == {"default": 120000}
    clear.assert_called()
