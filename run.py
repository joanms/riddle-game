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
    
with open("data/riddles.json") as riddle_file:
    riddle_list = json.load(riddle_file)    
    
def start():
    session['score'] = 0
    session['riddle_number'] = 0
    session["riddle_attempt"] = 1
    return session['score'], session['riddle_number'], session['riddle_attempt']

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
            start()
            return redirect(request.form["username"])
    return render_template("index.html")

# Playing the game
@app.route('/<username>', methods=['GET', 'POST'])
def play(username):
    data = riddle_list
    current_riddle = riddle_list[session["riddle_number"]]
    correct_answer = current_riddle["answer"]
    if request.method == 'POST':
        user_answer = request.form['user_input'].lower()

        """If the user answers correctly, the score increments and the next riddle displays.""" 
        """If they answer incorrectly on the first attempt they get another chance"""
        """If they answer incorrectly again, the next riddle displays"""

        if user_answer == correct_answer:
            if session['riddle_number'] < 9:
                session['riddle_number'] += 1
                current_riddle = riddle_list[session["riddle_number"]]
                session['score'] += 1
                session["riddle_attempt"] = 1
                flash('Well done!')
            else:
                flash("Game over!")
        elif session["riddle_attempt"] < 2:
            session["riddle_attempt"] += 1
            flash('You answered "{}", which was the wrong answer. Please try again.'.format(user_answer))
        else:
            if session['riddle_number'] < 9:
                session['riddle_number'] += 1
                current_riddle = riddle_list[session["riddle_number"]]
                session['riddle_attempt'] = 1
                flash('You answered "{}" but "{}" was the correct answer. Better luck on the next riddle.'.format(user_answer, correct_answer))
            else:
                flash("Game over!")

    return render_template('play.html', riddle_list=data, question=current_riddle["question"], username=username,
    riddle_number = session['riddle_number'], score = session['score'])

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)