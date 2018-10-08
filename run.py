import os
import json
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        if username not in open("data/users.txt").read():
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(username +"\n")
            return render_template("play.html")
        else:
            flash("That username is already taken. Please try another one.")
    return render_template("index.html")

@app.route('/play', methods=["GET", "POST"])
def play():
    json_data = []
    with open("riddles.json", "r") as json_file:
        json_data = json.load(json_file)
    return render_template("play.html", riddles=json_data)

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)