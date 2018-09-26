import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST" and request.form["username"] not in open("data/users.txt").read():
        with open("data/users.txt", "a+") as user_list:
            user_list.writelines(request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")

@app.route('/play')
def play():
    return render_template("play.html")

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)