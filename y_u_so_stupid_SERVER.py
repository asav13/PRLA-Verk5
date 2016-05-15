from flask import Flask
from flask import render_template
from flask import request
import y_u_so_stupid as fle
import json

app = Flask(__name__)

@app.route('/')
def hello():
    q = json.loads(fle.getRandomQuestion())
    question    = q['question']
    choices     = q['choices']
    
    return render_template('index.html',
                           question = question,
                           choices = choices)

@app.route('/', methods=['POST'])
def yuss():
    answer = request.form['answer']
    return hello()
    
if __name__ == '__main__':
    app.run()
