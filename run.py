import os
import json
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Start of code from my mentor, Chris Zielinski

# Get the info for the next riddle
def get_riddle(index):
    with open('data/riddles.json') as json_riddles:
        riddles = json.loads(json_riddles.read())
        return riddles[index] if index < 10 else None # Return None to avoid IndexError on the last riddle

# Initialise the game with some default values
def init_game(username):
    score = 0
    attempt = 1
    riddle = get_riddle(0)
    context = {
        'riddle_index': 0,
        'riddle': riddle['question'],
        'answer': riddle['answer'],
        'username': username,
        'current_score': score,
        'attempt': attempt
    }
    return context
    
# End of code from my mentor

# User logs in and the first question is displayed
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        if username not in open("data/users.txt").read():
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(username +"\n")
                context = init_game(username)
                return render_template("ready.html", context=context, username=username)
        else:
            flash("That username is already taken. Please try another one.")
    return render_template("index.html")

@app.route('/play/<username>', methods=["GET", "POST"])
def play(username):
    context = init_game(username)
    if request.method == "POST":
        riddle_index = 0
        riddle = get_riddle(riddle_index)
        user_answer = request.form.get("user_answer")
        correct_answer = riddle["answer"]
        correct = user_answer == correct_answer
        if user_answer != None:
            if correct:
                flash("Correct!")
            else:
                flash("{} was the wrong answer. Please try again.".format(user_answer))
    return render_template("play.html", context=context, username=username)

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)