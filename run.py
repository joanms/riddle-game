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
    
# Set initial variables - this code is by Joke Heyndels
def start():
    session['score'] = 0
    session['question_number'] = 1
    return session['score'], session['question_number']

# Game Play
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']   
    with open('data/users.txt', 'r') as user_list:
        current_users = user_list.read().splitlines()
    if username in current_users:
        flash("That username is taken. Please choose another one.")
    else:
        user_list = open("data/users.txt", "a")
        user_list.write(username + "\n")
        session['user'] = username
        start()
        return render_template('ready.html', username=username)
    return render_template("index.html")

        
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