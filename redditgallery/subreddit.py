import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from redditgallery.auth import login_required
from redditgallery.post import prepare_post

bp = Blueprint('subreddit', __name__, url_prefix='/r')


@bp.route('/<sub>/')
def nocount(sub):
	return redirect(url_for('subreddit.posts', sub=sub, count=current_app.config['STANDARD_LIMIT'], sort=current_app.config['STANDARD_SORT']))


@bp.route('/<sub>/<int:count>/')
def nosort(sub, count):
	return redirect(url_for('subreddit.posts', sub=sub, count=count, sort=current_app.config['STANDARD_SORT'])) 


@bp.route('/<sub>/<int:count>/<sort>/')
@login_required
def posts(sub, count, sort):
	try:
		subreddit = g.reddit.subreddit(sub)
		doGfy = False
		limit = count

		if "&" in sort:
			sortB = sort.split("&")
			sort = sortB[0]
			if sortB[1] == "gfycat":
				doGfy = True

		if "top" in sort:
			subr = subreddit.top(sort.split("@")[1], limit=limit)
		elif "controversial" in sort:
			subr = subreddit.controversial(sort.split("@")[1], limit=limit)
		elif sort == "hot":
			subr = subreddit.hot(limit=limit)
		elif sort == "rising":
			subr = subreddit.rising(limit=limit)
		elif sort == "new":
			subr = subreddit.new(limit=limit)
		elif sort == "gilded":
			subr = subreddit.gilded(limit=limit)
		else:
			abort(400)

		items = []

		for submission in subr:
			items.append(prepare_post(submission, doGfy))

		return render_template('gallery/gallery.html', pics=items)
	except IndexError:
		abort(400)



