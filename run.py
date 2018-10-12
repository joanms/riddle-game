import os
import json
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_riddle(index):
    with open("data/riddles.json", "r") as json_file:
        riddles = json.loads(json_file)
        return riddles[index]
        
# CHRIS' CODE START
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
# CHRIS' CODE END

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        if username not in open("data/users.txt").read():
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(username +"\n")
                return render_template("play.html", page_title="Play the Game!")
        else:
            flash("That username is already taken. Please try another one.")
    return render_template("index.html", page_title="Please select a username:")

@app.route('/play', methods=["GET", "POST"])
def play():
    return render_template("play.html")

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html", page_title="Leaderboard")
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)