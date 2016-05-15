from flask import Flask, render_template, request, url_for
import y_u_so_stupid as fle
import json

app = Flask(__name__)

correctAnswer = ''
score = 0
highscore = 0

@app.route('/')
def play():
    global correctAnswer
    
    q = json.loads(fle.getRandomQuestion())
    question            = q['question']
    choices             = q['choices']
    correctAnswer       = q['answer']
    
    return render_template('index.html',
                           question = question,
                           choices  = choices,
                           score    = score)

@app.route('/', methods=['POST'])
def game():
    global score
    global highscore
    
    answer = request.form['answer']
    if answer == correctAnswer:
        score += 10
        return play()
    else:
        if score > highscore:
            highscore = score
        return fail()

@app.route('/')
def fail():
    global score

    currScore = score
    score = 0
    return render_template('fail.html',
                           currScore        = currScore,
                           highscore        = highscore,
                           correctAnswer    = correctAnswer)
    
if __name__ == '__main__':
    app.run()
