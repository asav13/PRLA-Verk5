import select
import sys
import json
import y_u_so_stupid
import time
import argparse

'''
    ARGUMENT PARSING
'''
parser = argparse.ArgumentParser(description='Y U so stupid!?')
parser.add_argument('-q', '--questions', help='number of questions to run', type=int, nargs=1)

args = parser.parse_args()

'''
    MAIN FUNCTION
'''
def playCLI():
    score = 0
    if args.questions:
        numberOfQuestions = args.questions[0]
    else:
        numberOfQuestions = 10
    
    printAndFlush("~Welcome to 'y u so stupid?'~\nNow, don't be stupid mkey?\n\nAre you ready?\n...\n")

    for i in range(numberOfQuestions):
        question = json.loads(y_u_so_stupid.getRandomQuestion())

        printAndFlush(question['question'])
        
        for c in question['choices']:
            printAndFlush("{0}: {1}".format(question['choices'].index(c), c))
    
        playerAnswer = input()
        
        while playerAnswer not in ['0','1','2','3']:
            printAndFlush('y u so stupid..? Please enter a valid choice: 0, 1, 2 or 3')
            playerAnswer = input()
        printAndFlush("")
        
        if int(playerAnswer) == question['choices'].index(question['answer']):
            printAndFlush("CORRECT\n")
            score += 10
            
        else:
            printAndFlush("WRONG... y u so stupid?\nAnswer: {0}\n".format(question['answer']))
        
    printAndFlush("Your score is: {0}/100".format(int(score/(numberOfQuestions*10)*100)))

def printAndFlush(string):
    print(string)
    sys.stdout.flush()

playCLI()
