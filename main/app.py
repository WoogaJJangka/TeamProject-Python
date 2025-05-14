<<<<<<< HEAD
from flask import Flask, render_template
from game.game_manager import GameManager

game = GameManager()
app = Flask(__name__)

@app.route('/')
def index():
    board_matrix = game.get_board_matrix()
    current_color = game.get_current_player_color()
    return render_template('index.html', board=board_matrix, current_turn=current_color)
=======
from flask import Flask, render_template
from game.game_manager import GameManager

game = GameManager()
app = Flask(__name__)

@app.route('/')
def index():
    board_matrix = game.get_board_matrix()
    current_color = game.get_current_player_color()
    return render_template('index.html', board=board_matrix, current_turn=current_color)
>>>>>>> 03ef5a75298ff18032c20f31e4eb5562f738139d
