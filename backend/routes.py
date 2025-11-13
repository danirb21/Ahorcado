from flask import Flask
app =Flask(__name__)

@app.route("/gamescore")
def get_score():
    return "<h1>La puntuacion es..... X<h1>"