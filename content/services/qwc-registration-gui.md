+++
title = "Registration GUI"
menuTitle = "qwc-registration-gui"
weight = 14
+++


Provides an application form, so users can submit group membership requests.

These membership requests can then be approved or declined by an admin user in the [QWC configuration backend](https://github.com/qwc-services/qwc-admin-gui).


Setup
-----

Uses PostgreSQL connection service `qwc_configdb` (ConfigDB).

Setup PostgreSQL connection service file `pg_service.conf`:

```
host=localhost
port=5439
dbname=qwc_demo
user=qwc_admin
password=qwc_admin
sslmode=disable
```

Place this file in your home directory, or set the `PGSERVICEFILE` environment variable to point to the file.


Configuration
-------------

### Mailer

Set the `ADMIN_RECIPIENTS` environment variable to a comma separated list of admin users who should be notified of new registration requests (default: `None`).

* `MAIL_SERVER`: default ‘localhost’
* `MAIL_PORT`: default 25
* `MAIL_USE_TLS`: default False
* `MAIL_USE_SSL`: default False
* `MAIL_DEBUG`: default app.debug
* `MAIL_USERNAME`: default None
* `MAIL_PASSWORD`: default None
* `MAIL_DEFAULT_SENDER`: default None
* `MAIL_MAX_EMAILS`: default None
* `MAIL_SUPPRESS_SEND`: default app.testing
* `MAIL_ASCII_ATTACHMENTS`: default False

In addition the standard Flask `TESTING` configuration option is used by Flask-Mail in unit tests.

### Translations

Translation strings are stored in a JSON file for each locale in `translations/<locale>.json` (e.g. `en.json`). Add any new languages as new JSON files.

Set the `DEFAULT_LOCALE` environment variable to choose the locale for the application form and notifications (default: `en`).


Usage
-----

Run standalone application:

    python server.py

Registration form (if user is signed in):

    http://localhost:5032/register


Development
-----------

Install Python module for PostgreSQL:

    apt-get install python3-psycopg2

Create a virtual environment:

    virtualenv --python=/usr/bin/python3 .venv

Activate virtual environment:

    source .venv/bin/activate

Install requirements:

    pip install -r requirements.txt

Start local service:

    MAIL_SUPPRESS_SEND=True MAIL_DEFAULT_SENDER=from@example.com ADMIN_RECIPIENTS=admin@example.com python server.py
