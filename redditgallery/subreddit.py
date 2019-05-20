import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from redditgallery.auth import login_required
from redditgallery.post import render

import pprint

bp = Blueprint('subreddit', __name__, url_prefix='/r')

def getSubr(sub, sort, limit):
	subreddit = g.reddit.subreddit(sub)
	try:
		if "top" in sort:
			subr = subreddit.top(sort.split("@")[1], limit=limit)
		elif "controversial" in sort:
			subr = subreddit.controversial(sort.split("@")[1], limit=limit)
		elif "hot" in sort:
			subr = subreddit.hot(limit=limit)
		elif "rising" in sort:
			subr = subreddit.rising(limit=limit)
		elif "new" in sort:
			subr = subreddit.new(limit=limit)
		elif "gilded" in sort:
			subr = subreddit.gilded(limit=limit)
		else:
			abort(400)
		return subr
	except IndexError:
		return 'Index Error'

@bp.route('/getNext/', methods=['POST',])
def getNext():
	if request.method == 'POST':
		sort = request.form['sort']
		next = int(request.form['next'])
		subr = request.form['subr']
		doRender = int(request.form['render'])
		gfycat = request.form['gfycat']

		ids = []
		for submission in getSubr(subr, sort, next):
			ids.append(submission.id)

		if doRender == 1:
			return render(ids[-1], gfycat)

		return ids[-1]

	else:
		abort(405);

@bp.route('/<sub>/')
def nocount(sub):
	return redirect(url_for('subreddit.posts', sub=sub, sort=current_app.config['STANDARD_SORT']))

@bp.route('/<sub>/<sort>/')
@login_required
def posts(sub, sort):
	try:
		
		if g.user['show_gfycat'] == False:
			doGfy = 'false'
		else:
			doGfy = 'true'

		if "&" in sort:
			sortB = sort.split("&")
			sort = sortB[0]
			if sortB[1] == "gfycat":
				doGfy = 'true'
			elif sortB[1] == "noGfycat":
				doGfy = 'false'

		return render_template('gallery/gallery.html', gfy=doGfy, sort=sort, subr=sub)
	except IndexError:
		abort(400)



