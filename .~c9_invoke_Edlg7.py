import os
import json
from flask import Flask, flash, render_template, redirect, request, url_for, session

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
    
with open('data/riddles.json') as riddle_file:
    RIDDLES = json.load(riddle_file)    
    

@app.route('/')
def index():
    return render_template('index.html')
 
# The user logs in    
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        with open('data/users.txt', 'r') as user_list:
            current_users = user_list.read().splitlines()
        if username in current_users:
            flash('That username is taken. Please choose another one.')
        else:
            user_list = open('data/users.txt', 'a')
            user_list.write(username + '\n')
            session['user'] = username
            redirect(request.form["username"])
            session['riddle_number'] = 0
            session['attempt'] = 1
            new_riddle = RIDDLES[session["riddle_number"]]
            return render_template('play.html', username=username, question=new_riddle["question"], 
            riddle_number = session['riddle_number'], score = session['score'], attempt = session['attempt'])
    return render_template('index.html')


# Playing the game
@app.route('/<username>', methods=['GET', 'POST'])
def play(username):
    if request.method == 'POST' and session['riddle_number'] < 10:
        current_riddle = RIDDLES[session['riddle_number']]
        while session['riddle_number'] < 10:
            if request.form['user_input'].lower() == current_riddle['answer']:
                flash('Well done!')
                session['riddle_number'] += 1
                session['score'] += 1
            elif session['attempt'] == 1:
                flash('{} was the wrong answer. Please try again.'.format(session['user_answer']))
            else:
                flash('{} was the correct answer. Better luck on the next riddle.'.format(session['correct_answer']))
                session['riddle_number'] += 1
    new_riddle = RIDDLES[session["riddle_number"]]
    return render_template('play.html', question=new_riddle["question"], username=session['user'],
    riddle_number = session['riddle_number'], score = session['score'], attempt = session['attempt'])

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)