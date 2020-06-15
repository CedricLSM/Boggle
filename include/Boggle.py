from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from nltk.corpus import words

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
    getCorrectAnswer()

    makeBoard()
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

        #form 2D list of the board
        tmpWordLi = self.board.split(",")
        wordLi = []
        tmp = []
        for i in range(len(tmpWordLi)):
            if i%4==0 and i!=0:
                wordLi.append(tmp)
                tmp = []
            tmp.append(tmpWordLi[i])
        wordLi.append(tmp)

        #get a list of all english words with lengths 3 & 4
        mywords = [i.upper() for i in words.words() if len(i)>=3 and len(i)<=4]

        #build a trie for efficient search, using mywords
        trie = self.createTrie(mywords)

        #DFS to find all correct answers to match against player's answers
        m,n = len(wordLi),len(wordLi[0])
        finalWordLi = []
        for i in range(m):
            for j in range(n):
                self.findCorrectAnswer(wordLi,i,j,trie,"",finalWordLi)

        return ",".join(list(set(finalWordLi)))

    def createTrie(mywords):
        trie = {}
        for w in mywords:
            t = trie
            for c in w:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t["#"] = "#"
        return trie

    def findCorrectAnswer(self,wordLi,i,j,trie,path,finalWordLi):
        m,n = len(wordLi),len(wordLi[0])
        if '#' in trie:
            finalWordLi.append(path)
        if i<0 or i>=m or j<0 or j>=n or wordLi[i][j] not in trie:
            return
        tmp = wordLi[i][j]
        wordLi[i][j] ="@"
        self.findCorrectAnswer(wordLi, i+1, j, trie[tmp], path+tmp, finalWordLi)
        self.findCorrectAnswer(wordLi, i, j+1, trie[tmp], path+tmp, finalWordLi)
        self.findCorrectAnswer(wordLi, i-1, j, trie[tmp], path+tmp, finalWordLi)
        self.findCorrectAnswer(wordLi, i, j-1, trie[tmp], path+tmp, finalWordLi)

        self.findCorrectAnswer(wordLi, i+1, j+1, trie[tmp], path+tmp, finalWordLi)
        self.findCorrectAnswer(wordLi, i+1, j-1, trie[tmp], path+tmp, finalWordLi)
        self.findCorrectAnswer(wordLi, i-1, j-1, trie[tmp], path+tmp, finalWordLi)
        self.findCorrectAnswer(wordLi, i-1, j+1, trie[tmp], path+tmp, finalWordLi)
        wordLi[i][j] = tmp


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

@app.route("/games/find_latest")
def getLatestGameID():
    all_games = [boggle.json() for boggle in Boggle.query.all()]
    return str(all_games[-1]["gID"])

@app.route("/games/<int:gID>", methods=['PUT'])
def updateWordList(gID):
    games = Boggle.query.filter_by(gID=gID).first()
    data = request.get_json(["user_answer"])
    if data["user_answer"].upper().strip() not in games.user_answer:
        games.user_answer = games.user_answer+","+data["user_answer"].upper().strip()

    count = 0
    for crt_guess in games.user_answer.split(","):
        if crt_guess in games.correct_answer.split(","):
            count += 1
    games.user_score = count
    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred in updating the records."}), 500

    return jsonify({"Boggle": [games.json()]})

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