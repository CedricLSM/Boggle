from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/Boggle'
db = SQLAlchemy(app)
CORS(app)

class Boggle(db.Model):
    __tablename__ = 'Boggle'
    #game ID
    gID = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(100), nullable=False)
    user_score = db.Column(db.Integer,nullable=False)
    user_answer = db.Column(db.String(600), nullable=False)
    correct_answer = db.Column(db.String(600), nullable=False)




if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    app.run(host='0.0.0.0',port=7000, debug=True)