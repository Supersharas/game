from flask import Flask, url_for
from flask import render_template

from models import setup_db, Question, Category

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/chess')
def chess():
	return render_template('chess.html')