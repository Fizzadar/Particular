'''
Create initial migration for `User`, `UserAuthToken` and `Website` models.

Revision ID: d17ee1e02dc3
Revises:
Create Date: 2020-01-07 19:13:05.869637
'''

import sqlalchemy as sa

from alembic import op



# Revision identifiers, used by Alembic.
revision = 'd17ee1e02dc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=300), nullable=False),
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('date_created_utc', sa.DateTime(), nullable=True),
    sa.Column('date_login_utc', sa.DateTime(), nullable=True),
    sa.Column('session_key', sa.String(length=48), nullable=True),
    sa.Column('session_key_date_expiry_utc', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user_auth_token',
    sa.Column('token', sa.String(length=48), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('date_set_utc', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_table('website',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created_utc', sa.DateTime(), nullable=True),
    sa.Column('date_crawled_utc', sa.DateTime(), nullable=True),
    sa.Column('submitted_by_user_id', sa.Integer(), nullable=True),
    sa.Column('root_url', sa.String(length=300), nullable=False),
    sa.Column('allowed_domains', sa.Text(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['submitted_by_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('root_url')
    )
    op.create_table('website_up_vote',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('website_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['website_id'], ['website.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'website_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('website_up_vote')
    op.drop_table('website')
    op.drop_table('user_auth_token')
    op.drop_table('user')
    # ### end Alembic commands ###
