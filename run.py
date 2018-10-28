import os
import json
from flask import Flask, flash, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)


# User logs in and the first question is displayed
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
    context = init_game(username)
    if request.method == 'POST':
        riddle = get_riddle(riddle_index)
        user_answer = request.form.get('user_answer')
        correct_answer = riddle['answer']
        if user_answer != None: # This avoids an error when the user hasn't answered yet.
            correct = user_answer.lower() == correct_answer.lower() # The answer should not be case sensitive
            if correct:
                flash('Well done!')
                riddle_index += 1
            else:
                flash('{} was the wrong answer. Please try again.'.format(user_answer))
    return render_template('play.html', context=context, username=username)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)