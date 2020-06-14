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
            ID of a particular game
        board : str, optional
            The generated 4x4 board for the user to play a game on
        """

        self.gID = gID
        self.user_score = user_score
        self.user_answer = user_answer
        self.board = self.board
        if self.board == None:
            self.board = self.make_board()

        self.correct_answer = correct_answer
        if self.correct_answer == None:
            self.correct_answer = self.get_correct_answer()

        def get_correct_answer(self): 
            #TODO: Write function to create Trie and traverse the board using DFS to determine all correct answers
            return ""


        def make_board(self): 
            """
            Returns a 4x4 board.
            """
            #TODO: Generate a randomized 4x4 board to be returned
            board1 = "A,C,E,D,L,U,G,I,E,D,H,T,G,A,F,K"
            return board1

    def json(self):
        return {"gID": self.gID, "user_score":self.user_score,"board":self.board,"user_answer": self.user_answer, "correct_answer":self.correct_answer}



if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    app.run(host='0.0.0.0',port=7000, debug=True)