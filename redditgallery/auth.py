import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from redditgallery.db import get_db

import praw

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		accpassword = request.form['accpassword']
		client_id = request.form['client_id']
		client_secret = request.form['client_secret']
		
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif not accpassword:
			error = 'Reddit Gallery Account password is required.'
		elif not client_id:
			error = 'Client Id is required.'
		elif not client_secret:
			error = 'Client Secret is required.'
		elif db.execute(
			'SELECT id FROM accounts WHERE username = ?', (username,)
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			db.execute(
				'INSERT INTO accounts (username, password, accpassword, client_id, client_secret, show_nsfw) VALUES (?, ?, ?, ?, ?, ?)',
				(username, password, generate_password_hash(accpassword), client_id, client_secret, 0)
			)
			db.commit()
			return redirect(url_for('auth.login'))

		return render_template('auth/register.html', error=error)

	return render_template('auth/register.html')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        accpassword = request.form['accpassword']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM accounts WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['accpassword'], accpassword):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.user'))

        return render_template('auth/login.html', error=error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
		g.reddit = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM accounts WHERE id = ?', (user_id,)
		).fetchone()
		g.reddit = reddit = praw.Reddit(client_id=g.user['client_id'],
                     client_secret=g.user['client_secret'],
                     user_agent=current_app.config['USER_AGENT'],
					 password=g.user['password'],
					 username=g.user['username'])

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/user')
@login_required
def user():
	return render_template('auth/user.html')

@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
	msg = ''	

	if request.method == 'POST':
		nsfw = request.form['show_nsfw']
		pswd = request.form['password']
		if nsfw == 'true':
			nsfw = 1
		else:
			nsfw = 0
		db = get_db()
		if not pswd == '':
			db.execute('UPDATE accounts SET accpassword = ? WHERE id = ?', (generate_password_hash(pswd), g.user['id']))
		db.execute('UPDATE accounts SET show_nsfw = ? WHERE id = ?', (nsfw, g.user['id']))
		db.commit()
		msg = 'Settings saved succesfully!'
		return render_template('auth/settings.html', nsfw=nsfw, msg=msg)

	return render_template('auth/settings.html', nsfw=g.user['show_nsfw'], msg=msg)

@bp.route('/delete_account', methods=('GET', 'POST'))
@login_required
def delete_account():
	if request.method == 'POST':
		db = get_db()
		db.execute('DELETE FROM accounts WHERE id = ?', (g.user['id'],))
		db.commit()
		session.clear()
		return redirect(url_for('auth.register'))                                                                                                     
	return render_template('auth/delete.html')


