import os
import json
from flask import Flask, flash, render_template, redirect, request, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Error Handler code by Joke Heyndels
# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500 
    
    
# Define the data source
with open('data/riddles.json') as riddle_file:
    riddle_list = json.load(riddle_file)    
    
    
# Set the initial session variables
def start():
    session['score'] = 0
    session['riddle_number'] = 0
    session['riddle_attempt'] = 1
    return session['score'], session['riddle_number'], session['riddle_attempt']


# The user logs in
@app.route('/', methods=['GET', 'POST'])
def index():
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
            start()
            return redirect(request.form['username'])
    return render_template('index.html')


# Playing the game
@app.route('/<username>', methods=['GET', 'POST'])
def play(username):
    data = riddle_list
    current_riddle = riddle_list[session['riddle_number']]
    correct_answer = current_riddle['answer']
    if request.method == 'POST':
        user_answer = request.form['user_input'].lower()

        # Iterate through the riddles and then display the leaderboard
            
        # If the user answers correctly, the score increments and the next riddle displays unless all riddles have been answered
        if user_answer == correct_answer:
            session['score'] += 1
            if session['riddle_number'] < 24:
                session['riddle_number'] += 1
                current_riddle = riddle_list[session['riddle_number']]
                session['riddle_attempt'] = 1
                flash('Well done!')
            else:
                write_to_leaderboard()
                return redirect(url_for("leaderboard"))

        # If the user answers incorrectly on the first attempt they get another chance        
        elif session['riddle_attempt'] < 2:
            session['riddle_attempt'] += 1
            flash('You answered "{}", which was the wrong answer. Please try again.'.format(user_answer))
            
        # If the user answers incorrectly a second time, the next riddle displays unless all riddles have been answered   
        elif session['riddle_number'] < 24:
            session['riddle_number'] += 1
            current_riddle = riddle_list[session['riddle_number']]
            session['riddle_attempt'] = 1
            flash('You answered "{}" but "{}" was the correct answer. Better luck on the next riddle.'.format(user_answer, correct_answer))
        else:
            write_to_leaderboard()
            return redirect(url_for("leaderboard"))
    return render_template('play.html', riddle_list=data, question=current_riddle['question'], username=username,
    riddle_number = session['riddle_number'], score = session['score'])
    
    
# When the game is over, write the user's score to the leaderboard
@app.route('/write_to_leaderboard')
def write_to_leaderboard():
    if session:
        if session['riddle_number'] >= 24:
            with open('data/leaders.txt', 'a') as leaderboard:
                leaderboard.write('\n{}:{}'.format(str(session['user']), str(session['score'])))


# Sort the leaderboard in descending order of scores
# This function is by my mentor, Chris Zielinski
def get_leaders():
    with open('data/leaders.txt') as leaders:
        leaders = [line for line in leaders.readlines()[1:]]
        sorted_leaders = []
        for leader in leaders:
            tupe = (leader.split(':')[0].strip(), int(leader.split(':')[1].strip()))
            sorted_leaders.append(tupe)
            
        # Sort leaders on the second element of the tuple, reverse the sort, then return the top 10
        return sorted(sorted_leaders, key=lambda x: x[1])[::-1][:10]


@app.route('/leaderboard')
def leaderboard():
    leaders = get_leaders()
    
    # If a session is in progress, the leaderboard page includes the answer to the last question and the player's score
    if session:
        current_riddle = riddle_list[session['riddle_number']]
        return render_template('leaderboard.html', leaders=leaders, score = session['score'], correct_answer=current_riddle['answer'])
        
    # If a session is not in progress, the leaderboard page just shows the top-ranked players
    else:
        return render_template('leaderboard.html', leaders=leaders)
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')))