import select
import sys
import json
import y_u_so_stupid
import time

def playCLI():
    score = 0
    
    printAndFlush("~Welcome to 'y u so stupid?'~\nNow, don't be stupid mkey?\n\nAre you ready?\n...\n")

    for i in range(10):
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
        
    printAndFlush("Your score is: {0}/100".format(score))

def printAndFlush(string):
    print(string)
    sys.stdout.flush()



