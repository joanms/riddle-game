import os
import json
from flask import Flask, flash, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Error Handlers
# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500 

# Game Play
# The user logs in
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)
        session['user'] = request.form['username']
        return redirect(url_for('ready'))
    return render_template('index.html')
    
@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in'   
    
@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped'
    
@app.route('/ready')
def ready():
    return render_template('ready.html')

@app.route('/play/<username>', methods=['GET', 'POST'])
def play(username):
    if request.method == 'POST':
        user_answer = request.form.get('user_answer')
    return render_template('play.html', username=username)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)