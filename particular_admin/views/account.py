from flask import abort, redirect, render_template, url_for

from particular_admin.app import app
from particular_admin.auth import (
    get_current_user,
    login_as_user,
    logout_current_user,
    require_user_level,
)
from particular_admin.models.user import User, UserAuthToken
from particular_admin.settings import ADMIN_URL, USER_LEVEL
from particular_admin.util.email import send_email
from particular_admin.util.object import get_object_or_none
from particular_admin.util.request import pass_request_data


@app.route('/login', methods=('GET',))
def get_login():
    return render_template('login.html')


@app.route('/logout', methods=('GET',))
def get_logout():
    logout_current_user()
    return redirect(url_for('get_index'))


@app.route('/login', methods=('POST',))
@pass_request_data(('an_email',))
def post_login(an_email):
    if '@' not in an_email:
        abort(400, 'Invalid email address!')

    auth_token = UserAuthToken(email=an_email)
    auth_token.save()

    login_url = url_for('get_go_login', auth_token=auth_token.token)
    send_email(an_email, 'Your Particular login link', f'{ADMIN_URL}{login_url}')
    return 'Check your email!'


@app.route('/login/<auth_token>', methods=('GET',))
def get_go_login(auth_token):
    auth_token = UserAuthToken.query.get(auth_token)
    if not auth_token or not auth_token.is_valid():
        abort(400, 'Invalid auth token')

    user = get_object_or_none(User, email=auth_token.email)

    if not user:
        user = User(email=auth_token.email)
        user.save()

    auth_token.delete()
    login_as_user(user)

    return redirect(url_for('get_index'))


@app.route('/account', methods=('GET',))
@require_user_level(USER_LEVEL)
def get_account():
    return render_template('account.html')


@app.route('/account', methods=('POST',))
@require_user_level(USER_LEVEL)
@pass_request_data(('name',))
def post_account(name):
    user = get_current_user()
    user.name = name
    user.save()
    return redirect(url_for('get_account'))
