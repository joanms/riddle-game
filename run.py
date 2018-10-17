import os
import json
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Start of code from my mentor, Chris Zielinski

def get_riddle(index):
    with open('data/riddles.json') as json_riddles:
        riddles = json.loads(json_riddles.read())
        return riddles[index] if index < 10 else None # Return None to avoid IndexError on the last riddle

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
@app.route('/')
def index():
    if request.method == "POST":
        username = request.form["username"]
        if username not in open("data/users.txt").read():
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(username +"\n")
                context = init_game(username)
                return render_template("play.html", context=context)
        else:
            flash("That username is already taken. Please try another one.")
    return render_template("index.html")

@app.route('/play', methods=["GET", "POST"])
def play():
    return render_template("play.html")

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)