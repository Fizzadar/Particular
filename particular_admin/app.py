from os import path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from particular_admin import settings
from particular_admin.settings import DATABASE, DEBUG, SECRET_KEY


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
    .format(**DATABASE)
)
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=path.join('particular_admin', 'migrations'))


@app.context_processor
def inject_settings():
    return {
        'settings': settings,
    }
