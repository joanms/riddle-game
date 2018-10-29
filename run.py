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
    
# Load the riddles
def get_riddles():
    with open('data/riddles.json', 'r') as riddle_data:
        riddles_list = json.load(riddle_data)['riddles']
        return riddles_list
    
    
# Set the initial variables - this is based on code by Joke Heyndels
def start():
    session['score'] = 0
    session['riddle_number'] = 1
    session['attempt'] = 1
    session['riddles'] = get_riddles()
    return session['score'], session['riddle_number'], session['attempt'], session['riddles']

@app.route('/')
def index():
    return render_template('index.html')
 
# The user logs in    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    with open('data/users.txt', 'r') as user_list:
        current_users = user_list.read().splitlines()
    if username in current_users:
        flash('That username is taken. Please choose another one.')
    else:
        user_list = open('data/users.txt', 'a')
        user_list.write(username + '\n')
        session['user'] = username
        start()
        return render_template('ready.html', username=username)
    return render_template('index.html')

# Instructions for the user
@app.route('/ready')
def ready():
    return render_template('ready.html')

# Playing the game
@app.route('/play/<username>', methods=['GET', 'POST'])
def play(username):
    if session:
        riddle_number = session['riddle_number']
        data = session['riddles']
        score = session['score']
        attempt = session['attempt']
        return render_template('play.html', riddles=data, riddle_number=riddle_number, score=score, attempt=attempt)
    else:
        return redirect(url_for('index'))

# Checking the answers
@app.route('/play', methods=['POST'])
def check_answer():
    if session:
        session['correct_answer'] = request.form.get('correct_answer')
        session['user_answer'] = request.form.get('guess').lower()
        correct = session['correct_answer'] == session['user_answer']
        if correct:
            flash("Well done!")
    return render_template('play.html')


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)