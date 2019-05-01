
import praw
from flask import Flask, request, render_template, jsonify, json, redirect, url_for, abort, current_app, g
from flask.cli import with_appcontext
import sqlite3
import click



useragent = 'linux:slideshow_web:v1.0.0 (by /u/Kip-Bot)'



app = Flask(__name__)

conn = sqlite3.connect("accounts.db")
c = conn.cursor()

for row in c.execute('SELECT * FROM accounts'):
	reddit = praw.Reddit(client_id=row[2],
                     client_secret=row[3],
                     user_agent=useragent,
					 password=row[1],
					 username=row[0])

conn.close()


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404

@app.errorhandler(400)
def page_not_found(error):
    return render_template('error/400.html'), 400

@app.errorhandler(418)
def page_not_found(error):
    return render_template('error/418.html'), 418




@app.route('/')
def home():
	abort(418)


@app.route('/user')
def user():
	return render_template('misc/user.html', username=str(reddit.user.me()))


@app.route('/set_user', methods=['POST', 'GET'])
def setUser():
	global reddit
	if request.method == 'POST':
		try:
			conn = sqlite3.connect('accounts.db')
			c = conn.cursor()
			reddit = praw.Reddit(client_id=request.form['id'],
                     client_secret=request.form['secret'],
                     user_agent=useragent,
					 password=request.form['password'],
					 username=request.form['username'])
			reddit.user.me()
			
			c.execute('DELETE FROM accounts')
			conn.commit()

			acc = (request.form['username'], request.form['password'], request.form['id'], request.form['secret'])

			c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", acc)
			conn.commit()
			conn.close()

			return redirect(url_for('user'))
		except:
			conn.close()
			return render_template('login/login_error.html') #"<p style='color: red;'><b>False Login</b></p>" + loginText
	return render_template('login/login.html')#loginText


@app.route('/r/<path:sub>')
def posts(sub):
	path = sub.split("/")
	try:
		subreddit = reddit.subreddit(path[0])
		doGfy = False
		limit = path[1]
		sort = path[2]

		if "&" in sort:
			sortB = sort.split("&")
			sort = sortB[0]
			if sortB[1] == "gfycat":
				doGfy = True

		if "top" in sort:
			subr = subreddit.top(sort.split("@")[1], limit=int(limit))
		elif "controversial" in sort:
			subr = subreddit.controversial(sort.split("@")[1], limit=int(limit))
		elif sort == "hot":
			subr = subreddit.hot(limit=int(limit))
		elif sort == "rising":
			subr = subreddit.rising(limit=int(limit))
		elif sort == "new":
			subr = subreddit.new(limit=int(limit))
		elif sort == "gilded":
			subr = subreddit.gilded(limit=int(limit))
		else:
			abort(400)

		items = []

		for submission in subr:
			items.append(preparePost(submission, doGfy))

		return render_template('gallery/gallery.html', pics=items)
	except IndexError:
		abort(400)


@app.route('/p/<postId>')
def post(postId):
	try:
		return render_template('gallery/gallery.html', pics=[preparePost(reddit.submission(id=postId))])
	except:
		abort(400)


@app.route('/vote/<path:subpath>', methods=['POST', 'GET'])
def vote(subpath):
	try:
		if request.method == 'POST':
			sub = reddit.submission(id=request.form['id'])
			vtT = request.form['voteType']
		else:
			vt = subpath.split("@")
			sub = reddit.submission(id=vt[1])
			vtT = vt[0]
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


@app.route('/save/<postId>', methods=['POST', 'GET'])
def savePost(postId):
	if request.method == 'POST':
		postId = request.form['id']
	sub = reddit.submission(id=postId)
	if sub.saved == False:
		sub.save()
	else:
		sub.unsave()
	return 'succes'




def preparePost(submission, doGfy=True):
	try:
		url = submission.url
		pId = submission.id
		title = submission.title

		if 'https://imgur.com/a/' in url:	
			outp = render_template('gallery/imguralbum.html', TITLE=title, POSTID=pId, WEBID=url[20:])
		elif "comments" in url:
			outp = render_template('gallery/text.html', TITLE=title, POSTID=pId, TYPE='Text')
		elif "https://gfycat.com/" in url:
			if doGfy == False:
				outp = render_template('gallery/text.html', TITLE=title, POSTID=pId, TYPE='Gfycat')
			else:
				outp= render_template('gallery/gfycat.html', TITLE=title, POSTID=pId, WEBID=url.split("/")[-1])
		elif 'https://i.imgur.com/' in url and '.gifv' in url:
			outp = render_template('gallery/imgurpic.html', TITLE=title, POSTID=pId, WEBID=url[20:-5])
		else:
			out = ''
			if '.jpg' not in url and '.png' not in url and '.jpeg' not in url and '.gifv' not in url and '.gif' not in url:
				out = ".png"
			outp = render_template('gallery/imgfromsrc.html', SRC=url+out, POSTID=pId, TITLE=title)

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




if __name__ == '__main__':
	app.run(debug=True, port=8080)


