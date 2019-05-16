from flask import Flask, render_template

def page_not_found(e):
  return render_template('error/404.html'), 404

def bad_request(e):
    return render_template('error/400.html'), 400

def teapot(e):
    return render_template('error/418.html'), 418

def serverErr(e):
	return render_template('error/500.html'), 500
