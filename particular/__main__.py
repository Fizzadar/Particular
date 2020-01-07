#!/usr/bin/env python

import os

from flask.cli import main


if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'particular.app:app'
    main(as_module=True)
