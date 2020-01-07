from datetime import datetime, timedelta

from particular_admin.app import db
from particular_admin.settings import AUTH_TOKEN_EXPIRE_SECONDS, USER_LEVEL
from particular_admin.util.crypto import generate_key

from .base import Base

AUTH_TOKEN_EXPIRY = timedelta(seconds=AUTH_TOKEN_EXPIRE_SECONDS)


class UserAuthToken(db.Model, Base):
    token = db.Column(db.String(48), primary_key=True)
    email = db.Column(db.String(256))

    date_set_utc = db.Column(db.DateTime, default=datetime.utcnow)

    def is_valid(self):
        return datetime.utcnow() - self.date_set_utc < AUTH_TOKEN_EXPIRY

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_key()

        super(UserAuthToken, self).save(*args, **kwargs)


class User(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.String(300), nullable=False, unique=True)
    name = db.Column(db.String(300), nullable=False)

    level = db.Column(db.Integer, nullable=False, default=USER_LEVEL)

    date_created_utc = db.Column(db.DateTime, default=datetime.utcnow)
    date_login_utc = db.Column(db.DateTime)

    session_key = db.Column(db.String(48))
    session_key_date_expiry_utc = db.Column(db.DateTime)

    def __str__(self):
        return f'User: {self.email} ({self.name})'

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.email.split('@')[0]

        super(User, self).save(*args, **kwargs)
