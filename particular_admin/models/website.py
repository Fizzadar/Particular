from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy import func, select
from sqlalchemy.orm import column_property

from particular_admin.app import db
from particular_admin.settings import WEBSITE_HASH_IDS_SALT

from .base import Base, HashIdsBase


class WebsiteUpVote(db.Model, Base):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), primary_key=True)


class Website(db.Model, Base, HashIdsBase):
    HASH_IDS_SALT = WEBSITE_HASH_IDS_SALT

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    date_created_utc = db.Column(db.DateTime, default=datetime.utcnow)
    date_crawled_utc = db.Column(db.DateTime)

    submitted_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submitted_by_user = db.relationship('User')

    root_url = db.Column(db.String(300), nullable=False, unique=True)
    allowed_domains = db.Column(db.Text, nullable=False)

    active = db.Column(db.Boolean, nullable=False, default=False)

    upvote_user_ids = column_property(
        select([func.group_concat(WebsiteUpVote.user_id)])
        .where(WebsiteUpVote.website_id == id)
        .correlate_except(WebsiteUpVote),
        deferred=True,
    )

    class InvalidRootUrlError(Base.ValidationError):
        pass

    @property
    def allowed_domains_list(self):
        return self.allowed_domains.split()

    @property
    def upvote_userids(self):
        return [int(i) for i in self.upvote_user_ids.split(',')]

    def __str__(self):
        return f'Website: {self.root_url}'

    def save(self, *args, **kwargs):
        url = urlparse(self.root_url)
        if not url.scheme or not url.netloc:
            raise self.InvalidRootUrlError(f'{self.root_url} is not a valid URL!')

        if url.scheme != 'https':
            raise self.InvalidRootUrlError('All URLs must be https!')

        self.root_url = f'{url.scheme}://{url.netloc}'

        if not self.allowed_domains:
            self.allowed_domains = f'{url.netloc}\n'

        super(Website, self).save(*args, **kwargs)
