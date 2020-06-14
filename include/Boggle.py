from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/Boggle'
db = SQLAlchemy(app)
CORS(app)

class Boggle(db.Model):
    """
    A class to handle the logic of the game

    ...

    Parameters
    ----------
    user_score : int
        Score a user gets
    user_answer : str
        The answer submitted by a user
    correct_answer : str, optional
        All the correct answer contained in the board
    gID : int
        ID of a particular game (set to auto-increment in SQL script)
    board : str
        The generated 4x4 board for the user to play a game on (default board will be generated)

    Methods
    -------
    get_correct_answer()

    make_board()
        Returns a 4x4 wordlist in str form
    json()
        Returns the Boggle object in JSON form
    """

    __tablename__ = 'Boggle'
    gID = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(100), nullable=False)
    user_score = db.Column(db.Integer,nullable=False)
    user_answer = db.Column(db.String(600), nullable=False)
    correct_answer = db.Column(db.String(600), nullable=False)

    def __init__(self, user_score, user_answer, correct_answer=None, gID=None,board=None):
        """
        Parameters
        ----------
        user_score : int
            Score a user gets
        user_answer : str
            The answer submitted by a user
        correct_answer : str, optional
            All the correct answer contained in the board
        gID : int, optional
            ID of a particular game (set to auto-increment in SQL script)
        board : str, optional
            The generated 4x4 board for the user to play a game on (default board will be generated)
        """

        self.gID = gID
        self.user_score = user_score
        self.user_answer = user_answer
        self.board = self.board
        if self.board == None:
            self.board = self.makeBoard()

        self.correct_answer = correct_answer
        if self.correct_answer == None:
            self.correct_answer = self.getCorrectAnswer()

    def getCorrectAnswer(self): 
        #TODO: Write function to create Trie and helper function to traverse the board using DFS to determine all correct answers
        return ""


    def makeBoard(self): 
        """
        Returns a 4x4 board
        """
        #TODO: Generate a randomized 4x4 board to be returned
        board1 = "A,C,E,D,L,U,G,I,E,D,H,T,G,A,F,K"
        return board1

    def json(self):
        """
        Returns the Boggle object in JSON form
        """
        return {"gID": self.gID, "user_score":self.user_score,"board":self.board,"user_answer": self.user_answer, "correct_answer":self.correct_answer}

"""
App routes to manipulate Boggle game information via CRUD
"""

@app.route("/games")
def getAllGames():
    return jsonify({"Boggle": [boggle.json() for boggle in Boggle.query.all()]})

@app.route("/games/<int:gID>")
def getGame(gID):
    curr_game = Boggle.query.filter_by(gID=gID).first()
    if curr_game:
        return jsonify(curr_game.json())
    return jsonify({"message": "Game not found."}), 404

@app.route("/games", methods=['POST'])
def createGame():
    data = request.get_json()
    boggle = Boggle(**data)
    try:
        db.session.add(boggle)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the game."}), 500

    return jsonify(boggle.json()), 201

if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal.
    app.run(host='0.0.0.0',port=7000, debug=True)