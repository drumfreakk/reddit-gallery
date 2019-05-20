import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from redditgallery.auth import login_required

bp = Blueprint('post', __name__, url_prefix='/p')

def render(postId, gfycat):
	submission = g.reddit.submission(id=postId)
	try:
		url = submission.url
		pId = submission.id
		title = submission.title

		if submission.over_18 == True and g.user['show_nsfw'] == False:
			outp = render_template('gallery/pictures/nonPicture.html', TITLE=title, POSTID=pId, TYPE='NSFW')
		elif 'https://imgur.com/a/' in url:	
			outp = render_template('gallery/pictures/imguralbum.html', TITLE=title, POSTID=pId, WEBID=url[20:])
		elif "comments" in url:
			outp = render_template('gallery/pictures/nonPicture.html', TITLE=title, POSTID=pId, TYPE='Text')
		elif "https://gfycat.com/" in url:
			if gfycat == 'false':
				outp = render_template('gallery/pictures/nonPicture.html', TITLE=title, POSTID=pId, TYPE='Gfycat')
			else:
				outp= render_template('gallery/pictures/gfycat.html', TITLE=title, POSTID=pId, WEBID=url.split("/")[-1])
		elif 'https://i.imgur.com/' in url and '.gifv' in url:
			outp = render_template('gallery/pictures/imgurpic.html', TITLE=title, POSTID=pId, WEBID=url[20:-5])
		else:
			if 'i.imgur.com/' in url or 'i.redd.it/' in url:
				out = ''
				if '.jpg' not in url and '.png' not in url and '.jpeg' not in url and '.gifv' not in url and '.gif' not in url:
					out = ".png"
				outp = render_template('gallery/pictures/imgfromsrc.html', TITLE=title, POSTID=pId, SRC=url+out)
			else:
				outp = render_template('gallery/pictures/nonPicture.html', TITLE=title, POSTID=pId, TYPE='False')

		if submission.saved == True:
			outp = outp.replace('Save', 'Unsave').replace('notsave', 'save')
		if submission.likes == True:
			outp = outp.replace('notUp', 'up')
		elif submission.likes == False:
			outp = outp.replace('notDown', 'down')

		return outp
	except AttributeError:
		print("AttributeError")
		return 'AttributeError\n'

@bp.route('/render/', methods=['POST',])
def prepare_post():
	if request.method == 'POST':
		return render(request.form['postId'], request.form['gfyCat'])
	else:
		abort(405)

@bp.route('/<postId>')
@login_required
def post(postId):
	try:
		return render_template('gallery/singlePicture.html', item=postId)
	except:
		abort(400)


@bp.route('/<postId>/vote', methods=['POST',])
def vote(postId):
	try:
		if request.method == 'POST':
			sub = g.reddit.submission(id=postId)
			vtT = request.form['voteType']
		else:
			abort(405)
		if vtT == "up":
			if sub.likes == True:
				sub.clear_vote()
			else:
				sub.upvote()
		elif vtT == "down":
			if sub.likes == False:
				sub.clear_votes()
			else:
				sub.downvote()
		elif vtT == "clear":
			sub.clear_vote()
		else:
			abort(400)
		return 'succes'
	except IndexError:
		abort(400)


@bp.route('/<postId>/save', methods=['POST',])
def savePost(postId):
	if request.method == 'POST':
		sub = g.reddit.submission(id=postId)
	else:
		abort(405)
	if sub.saved == False:
		sub.save()
	else:
		sub.unsave()
	return 'succes'


