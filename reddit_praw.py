import praw
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("accounts.db")
c = conn.cursor()

for row in c.execute('SELECT * FROM accounts'):
	reddit = praw.Reddit(client_id=row[2],
                     client_secret=row[3],
                     user_agent='linux:slideshow_web:v1.0.0 (by /u/Kip-Bot)',
					 password=row[1],
					 username=row[0])

conn.close()

imguralbum = '<center><iframe allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true" style="height: 700px; width: 500px; margin: 10px 0px; padding: 0px;" class="imgur-embed-iframe-pub imgur-embed-iframe-pub-a-AAAAA-true-500" scrolling="no" src="https://imgur.com/a/AAAAA/embed?pub=true&amp;ref=https%3A%2F%2Fimgur.com%2Fa%2FAAAAA&amp;analytics=false&amp;w=500" id="imgur-embed-iframe-pub-a-AAAAA"></iframe></center>'

imgurpic = '<center><blockquote class="imgur-embed-pub" lang="en" data-id="AAA" data-context="false"><a href="//imgur.com/AAA">What the Event Horizon Telescope didn&#39;t capture (nyuunzi) [EHT]</a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script></center>'

gfycat = '''<center><div style='position:relative; padding-bottom:calc(42.19% + 44px)'><iframe src='https://gfycat.com/ifr/AAA' frameborder='0' scrolling='no' width='100%' height='100%' style='position:absolute;top:0;left:0;' allowfullscreen></iframe></div></center>'''

pic = '<center><div class="votes"><a href="localhost:8080/vote/up@BBB" target="_blank">Upvote</a><a href="localhost:8080/vote/clear@BBB" target="_blank">Clear vote</a><a href="localhost:8080/vote/down@BBB" target="_blank">Downvote</a><a href="localhost:8080/save/BBB" target="_blank">Save</a></div><img class="pic" height="1080" src="AAA"></center>'

text = "<center><p style='color:white;'><b>Text Post: AAA</b></p></center>"

loginText = '''  
	<body>	
	<form method="post">
    	<label for="username">Username</label>
    	<input name="username" id="username" required>
		</br>
    	<label for="password">Password</label>
    	<input type="password" name="password" id="password" required>
		</br>

		<label for="id">Id</label>
    	<input type="id" name="id" id="id" required>
		</br>
		
		<label for="secret">Secret</label>
    	<input type="secret" name="secret" id="secret" required>
		</br>
		
    	<input type="submit" value="Register">
	</form>
	</body>
'''

@app.route('/test')
def test():
	return render_template('base.html')

@app.route('/')
def home():
	return 'progress'

@app.route('/user')
def user():
	print(reddit.user.me())
	return "hi"

@app.route('/set_user', methods=['POST', 'GET'])
def setUser():
	global reddit
	if request.method == 'POST':
		try:
			conn = sqlite3.connect('accounts.db')
			c = conn.cursor()
			reddit = praw.Reddit(client_id=request.form['id'],
                     client_secret=request.form['secret'],
                     user_agent='linux:slideshow_web:v1.0.0 (by /u/Kip-Bot)',
					 password=request.form['password'],
					 username=request.form['username'])
			reddit.user.me()
			
			c.execute('DELETE FROM accounts')
			conn.commit()

			acc = (request.form['username'], request.form['password'], request.form['id'], request.form['secret'])

			c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", acc)
			conn.commit()
			conn.close()

			return 'Succes!'# + reddit.user.me()
		except:
			conn.close()
			return "<p style='color: red;'><b>False Login</b></p>" + loginText
	return loginText

@app.route('/<path:sub>')
def posts(sub):
	path = sub.split("/")
	try:
		return getPosts(path[0], path[1], path[2])
	except IndexError:
		return "Format: localhost:8080/sub/[subreddit]/[no. posts to show]/[sort(@time)]"

@app.route('/vote/<path:subpath>')
def vote(subpath):
	vt = subpath.split("@")
	sub = reddit.submission(id=vt[1])
	if vt[0] == "up":
		sub.upvote()
	elif vt[0] == "down":
		sub.downvote()
	elif vt[0] == "clear":
		sub.clear_vote()
	else:
		return "false vote type"
	return "succes"

@app.route('/save/<postId>')
def savePost(postId):
	sub = reddit.submission(id=postId)
	sub.save()
	return 'succes'

def getPosts(sub, limit, sort):
	subreddit = reddit.subreddit(sub)

	doGfy = False

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
		return "error"	

	items = []

	for submission in subr:
		try:
			url = submission.url
			if 'https://imgur.com/a/' in url:
				outp = imguralbum.replace("AAAAA", url[20:])
			elif "comments" in url:
				outp = text.replace("AAA", submission.title)
			elif "https://gfycat.com/" in url:
				if doGfy == False:
					outp = text.replace("Text", "Gfycat").replace("AAA", submission.title)
				else:
					outp= gfycat.replace("AAA", url.split("/")[-1])
			else:
				out = ''
				if '.jpg' not in url and '.png' not in url and '.jpeg' not in url:
					out = ".png"
				outp = pic.replace("AAA", url + out).replace("BBB", submission.id)
			outp += "</br>\n"
			items.append(outp)
		except AttributeError:
			continue
	return render_template('base.html', pics=items)

if __name__ == '__main__':
	app.run(debug=True, port=8080)


