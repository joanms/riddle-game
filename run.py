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
    
with open("data/riddles.json") as riddle_file:
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
            return render_template('play.html', username=username)
    return render_template('index.html')

# Set the initial variables
def start():
    session['score'] = 0
    session['riddle_number'] = 1
    session['attempt'] = 1
    return render_template('play.html')

# Playing the game
@app.route('/play', methods=['POST'])
def play():
    if session:
        riddle_number = session['riddle_number']
        score = session['score']
        attempt = session['attempt']
        if request.method == 'POST':
            session['correct_answer'] = request.form.get("correct_answer")
            session['user_answer'] = request.form.get("user_input").lower()
            while session['riddle_number'] < 10:
                if session['correct_answer'] == session['user_answer']:
                    flash("Well done!")
                    session['question_number'] += 1
                    session['score'] += 1
                elif session['attempt'] == 1:
                    flash("{} was the wrong answer. Please try again.".format(session['user_answer']))
                else:
                    flash("{} was the correct answer. Better luck on the next riddle.".format(session['correct_answer']))
                    session['question_number'] += 1
        return render_template('play.html', riddle_number=riddle_number, score=score, attempt=attempt)
    else:
        return redirect(url_for('index'))


# Checking the answers
@app.route('/play', methods=['POST'])
def check_answer():
    if session:
            return redirect(url_for("play"))
    else:
        return redirect(url_for("index"))
        

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)