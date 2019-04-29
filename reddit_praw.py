import praw
from flask import Flask, request, render_template, jsonify, json
import sqlite3

import pprint

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

start = "<center id='POSTID'><p class='title'>TITLE</p>"

end = '''<div class="votes"><a href='#POSTID' onclick="vote('up', 'POSTID')" class='notUp' id='POSTIDup'>Upvote </a><a href='#POSTID' onclick="vote('clear', 'POSTID')" class='clear' id='POSTIDclear'>Clear vote </a><a href='#POSTID' onclick="vote('down', 'POSTID')" class='notDown' id='POSTIDdown'>Downvote </a><a onclick='save("POSTID")' href='#POSTID' class='notSave' id='POSTIDsave'>Save</a></div></center>'''


imguralbum = start + '<iframe id="POSTID" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true" style="height: 700px; width: 500px; margin: 10px 0px; padding: 0px;" class="imgur-embed-iframe-pub imgur-embed-iframe-pub-a-WEBID-true-500" scrolling="no" src="https://imgur.com/a/WEBID/embed?pub=true&amp;ref=https%3A%2F%2Fimgur.com%2Fa%2FWEBID&amp;analytics=false&amp;w=500" id="imgur-embed-iframe-pub-a-WEBID"></iframe>' + end

imgurpic = start + '<blockquote class="imgur-embed-pub" lang="en" data-id="WEBID" data-context="false"><a href="//imgur.com/WEBID"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>' + end

gfycat = start + '''<div style='position:relative; padding-bottom:calc(42.19% + 44px)'><iframe src='https://gfycat.com/ifr/WEBID' frameborder='0' scrolling='no' width='100%' height='100%' style='position:absolute;top:0;left:0;' allowfullscreen></iframe></div>''' + end

pic = start + '''<img class="pic" height="1080" src="SRC">''' + end

text = "<center><p class='title'>Text Post: TITLE</p>" + end

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

@app.route('/')
def home():
	return 'progress'

@app.route('/user', methods=['GET', 'POST'])
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

@app.route('/vote/<path:subpath>', methods=['POST', 'GET'])
def vote(subpath):
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
		return "false vote type"
	return "succes"

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
		#pprint.pprint(vars(submission))
		try:
			url = submission.url
			if 'https://imgur.com/a/' in url:
				outp = imguralbum.replace("WEBID", url[20:])
			elif "comments" in url:
				outp = text.replace("WEBID", submission.title)
			elif "https://gfycat.com/" in url:
				if doGfy == False:
					outp = text.replace("Text", "Gfycat").replace("WEBID", submission.title)
				else:
					outp= gfycat.replace("WEBID", url.split("/")[-1])
			elif 'https://i.imgur.com/' in url and '.gifv' in url:
				outp = imgurpic.replace("WEBID", url[20:-5])
			else:
				out = ''
				if '.jpg' not in url and '.png' not in url and '.jpeg' not in url and '.gifv' not in url and '.gif' not in url:
					out = ".png"
				outp = pic.replace("SRC", url + out)
			outp += "</br>\n"
			outp = outp.replace("TITLE", submission.title).replace("POSTID", submission.id)
			if submission.saved == True:
				outp = outp.replace('Save', 'Unsave').replace('notSave', 'save')
			if submission.likes == True:
				outp = outp.replace('notUp', 'up')
			elif submission.likes == False:
				outp = outp.replace('notDown', 'down')
			items.append(outp)
		except AttributeError:
			print("AttributeError")
			continue	
	return render_template('base.html', pics=items)

if __name__ == '__main__':
	app.run(debug=True, port=8080)


