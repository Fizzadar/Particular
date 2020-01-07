#!/usr/bin/env python

import os

from flask.cli import main

from particular_admin import auth, csrf  # noqa: F401
from particular_admin.views import account, error, website  # noqa: F401


if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'particular_admin.app:app'
    main(as_module=True)
