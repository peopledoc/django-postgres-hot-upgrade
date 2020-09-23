# django-postgres-hot-upgrade

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
