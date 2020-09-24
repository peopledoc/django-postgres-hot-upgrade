# django-postgres-hot-upgrade

[![Deployed to PyPI](https://img.shields.io/pypi/v/django-postgres-hot-upgrade?logo=pypi&logoColor=white)](https://pypi.org/pypi/django-postgres-hot-upgrade)
[![Deployed to PyPI](https://img.shields.io/pypi/pyversions/django-postgres-hot-upgrade?logo=pypi&logoColor=white)](https://pypi.org/pypi/django-postgres-hot-upgrade)
[![Continuous Integration](https://img.shields.io/github/workflow/status/peopledoc/django-postgres-hot-upgrade/CI?logo=github)](https://github.com/peopledoc/django-postgres-hot-upgrade/actions?workflow=CI)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)


Let Django clear its PostgreSQL extensions OIDs cache, making it possible to update
the PostgreSQL version to a new major version on the fly.

## The how
```console
$ pip install django-postgres-hot-upgrade
```
```python
INSTALLED_APPS = [
    ...,
    # Warning: django_postgres_hot_upgrade requires to be placed before
    # django.contrib.postgres otherwise it will not work.
    'django_postgres_hot_upgrade',
    'django.contrib.postgres',
    ...,
]
```

## The why

PostgreSQL keeps internal ids of for various objects
([OIDs](https://www.postgresql.org/docs/current/datatype-oid.html)). This includes
loaded extentions. In order to interact with those extensions, Django needs to know
these IODs, so it loads them and, in order to avoid [unneeded
requests](https://code.djangoproject.com/ticket/28334?), it caches them in memory for
the duration of the process.

Several PostgreSQL servers running the same version of PostgreSQL will have consistent
OIDs but when you upgrade, OIDs can change. If one uses a PostgreSQL load balancer such
as [pgbouncer](https://www.pgbouncer.org/) or [pgpool](https://www.pgpool.net), one
could be tempted to migrate between major PostgreSQL versions on the fly, avoinding
downtime. Indeed, for sufficiently recent versions of PostgreSQL, this would work, apart
from the OID problem: if OIDs change, Django needs to update its cache.

`django_postgres_hot_upgrade` memorizes the postgres version of the server after each
connection. When the version is updated, it clears the internal Django OIDs cache,
forcing Django to fetch the new values.


## The rest

**Compatibility**: Please refer to versions of Python and Django tested in
[tox.ini](tox.ini).

**License**: [MIT](LICENSE)

**Code of Conduct**: This project is placed under the [Contributor
Coveneant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). Please
report any abuse to `joachim.jablon at people-doc.com`.


## [Maintainers] The ugly part

Apart from its unit tests, this package has an integration test. In order to test the
feature, we need to simulate a change of OIDs caused by a live update from PG10 to PG12
in a controlled CI environment. This is the most fragile part of the lib, and the most
likely to break in the future. Here's what you need to know:

- `docker-compose.yml` define two databases `postgres10` and `postgres12` listening on
  5432 and 5433 respectively.
- `tests/django_settings.py` define a `default` database using libpq envvars. Note that
  in the settings, we requests the tests to run on the normal database instead of
  dedicated `test_<foo>` database.
- The OIDs are created by Postgres when installing the extensions. This happens in
  `tests/migrations/0001_initial.py`. The `DJANGO_REVERSE_OPERATIONS` env var controls
  the order of the 2 extensions creation. Running the PG10 migration in normal order
  and the PG12 migration in reverse order ensures the OIDs will be different.
- The `runtests` script ensure the migrations run on both databases in the decided
  order, then launches the test. Without this, the integration test would likely fail
  because the OIDs would be the same in the two databases.
- `tox` calls `runtests`.
- GitHub Actions call `tox`.

The following work to launch tests locally:

- run `tox` or `runtests` on fresh databases
- run `pytests` if you know the OIDs are already properly set on the 2 databases
