from flask import Flask, request, render_template, jsonify
from uuid import uuid4


from boggle import BoggleGame
from wordlist import WordList

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}

@app.get("/")
def homepage():
    """Show board.
        >>>

    """

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return {"gameId": game_id, "board": game.board}

@app.post("/api/score-word")
def score_word():
    """ Checks if word is on list and on board
    """

    word = request.json["word"]
    game_id = request.json["gameId"]
    game = games[game_id]

    word_in_list = game.is_word_in_word_list(word)
    word_in_board =  game.check_word_on_board(word)

    if word_in_list and word_in_board:
        return jsonify({"result": "ok"})
    elif not word_in_list:
        return jsonify({"result": "not-word"})
    elif not word_in_board:
        return jsonify({"result": "not-on-board"})
