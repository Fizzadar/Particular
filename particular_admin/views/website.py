from flask import abort, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, undefer

from particular_admin.app import app
from particular_admin.auth import get_current_user, require_user_level
from particular_admin.models.website import Website, WebsiteUpVote
from particular_admin.settings import MODERATOR_LEVEL, USER_LEVEL
from particular_admin.util.object import get_object_or_404
from particular_admin.util.request import pass_request_data


def do_get_websites(**filters):
    websites = Website.query
    active_website_count = websites.filter_by(active=True).count()
    pending_website_count = websites.filter_by(active=False).count()

    websites = websites.filter_by(**filters)
    websites = websites.options(
        joinedload('submitted_by_user'),
        undefer('upvote_user_ids'),
    )

    return render_template(
        'website/list.html',
        websites=websites,
        active_website_count=active_website_count,
        pending_website_count=pending_website_count,
        filters=filters,
    )


@app.route('/websites', methods=('GET',))
def get_websites():
    return do_get_websites()


@app.route('/websites/active', methods=('GET',))
def get_active_websites():
    return do_get_websites(active=True)


@app.route('/websites/pending', methods=('GET',))
def get_pending_websites():
    return do_get_websites(active=False)


@app.route('/websites/submit', methods=('GET',))
@require_user_level(USER_LEVEL)
def get_submit_website():
    return render_template('website/submit.html')


@app.route('/websites/submit', methods=('POST',))
@require_user_level(USER_LEVEL)
@pass_request_data(('root_url',))
def post_submit_website(root_url):
    new_website = Website(
        root_url=root_url,
        submitted_by_user=get_current_user(),
    )

    try:
        new_website.save()
    except Website.InvalidRootUrlError as e:
        abort(400, e)
    except IntegrityError:
        abort(400, 'This website already exists!')

    return redirect(url_for('get_websites'))


@app.route('/websites/<hashed_id>/upvote', methods=('POST',))
@require_user_level(USER_LEVEL)
def post_upvote_website(hashed_id):
    website = get_object_or_404(Website, hashed_id=hashed_id)
    user = get_current_user()

    vote = WebsiteUpVote(
        user_id=user.id,
        website_id=website.id,
    )

    try:
        vote.save()
    except IntegrityError:
        abort(400, 'You cannot vote for the same website twice!')

    return redirect(url_for('get_websites'))


@app.route('/websites/<hashed_id>/unvote', methods=('POST',))
@require_user_level(USER_LEVEL)
def post_unvote_website(hashed_id):
    website = get_object_or_404(Website, hashed_id=hashed_id)
    user = get_current_user()

    vote = get_object_or_404(
        WebsiteUpVote,
        user_id=user.id,
        website_id=website.id,
    )
    vote.delete()

    return redirect(url_for('get_websites'))


@app.route('/websites/<hashed_id>', methods=('GET',))
@require_user_level(MODERATOR_LEVEL)
def get_edit_website(hashed_id):
    website = get_object_or_404(Website, hashed_id=hashed_id)
    return render_template('website/edit.html', website=website)


@app.route('/websites/<hashed_id>', methods=('POST',))
@require_user_level(MODERATOR_LEVEL)
@pass_request_data(('root_url', 'allowed_domains'))
@pass_request_data(('active',), required=False)
def post_edit_website(root_url, allowed_domains, active, hashed_id):
    website = get_object_or_404(Website, hashed_id=hashed_id)
    website.root_url = root_url
    website.allowed_domains = allowed_domains
    website.active = active == 'on'

    try:
        website.save()
    except Website.InvalidRootUrlError as e:
        abort(400, e)
    except IntegrityError:
        abort(400, 'This website already exists!')

    return redirect(url_for('get_edit_website', hashed_id=hashed_id))
