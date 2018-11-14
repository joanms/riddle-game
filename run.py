import os
import json
from flask import Flask, flash, render_template, redirect, request, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Error Handlers
# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500 
    
max_attempts = 2

with open("data/riddles.json") as riddle_file:
    riddle_list = json.load(riddle_file)    
  
    
@app.route("/", methods=["GET", "POST"])
def index():
    """The user logs in"""
    """Handle POST request"""
    if request.method == "POST":
        username = request.form["username"]
        with open("data/users.txt", "r") as user_list:
            current_users = user_list.read().splitlines()
        if username in current_users:
            flash("That username is taken. Please choose another one.")
        else:
            user_list = open("data/users.txt", "a")
            user_list.write(username + "\n")
            session["user"] = username
            return redirect(request.form["username"])
    return render_template("index.html")

# Playing the game
@app.route('/<username>', methods=['GET', 'POST'])
def play(username):
    data = riddle_list
    session['score'] = 0
    session['riddle_number'] = 0
    session["riddle_attempts"] = max_attempts
    current_riddle = riddle_list[session["riddle_number"]]
    correct_answer = current_riddle["answer"]
    if request.method == 'POST' and session['riddle_number'] < 10:
        user_answer = request.form['user_input'].lower()
        if user_answer == correct_answer:
            session['riddle_number'] += 1
            current_riddle = riddle_list[session["riddle_number"]]
            correct_answer = current_riddle["answer"]
            session['score'] += 1
            flash('Well done!')
        elif not session["riddle_attempts"]:
            session['riddle_number'] += 1
            current_riddle = riddle_list[session["riddle_number"]]
            correct_answer = current_riddle["answer"]
            session['attempt'] = 1
            flash('{} was the correct answer. Better luck on the next riddle.'.format(correct_answer))
        else:
            session["riddle_attempts"] -= 1
            flash('{} was the wrong answer. Please try again.'.format(user_answer))
    return render_template('play.html', riddle_list=data, question=current_riddle["question"], username=username,
    riddle_number = session['riddle_number'], score = session['score'])

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)