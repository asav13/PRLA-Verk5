import sys
import json
from y_u_so_stupid import getRandomQuestion

def playCLI():
    score = 0
    
    print("Welcome to 'y u so stupid?'")
    print("Now don't be stupid mkey?\n")
    print('Are you ready?')
    print('...')
    sys.stdout.flush()

    for i in range(10):
        question = json.loads(getRandomQuestion())

        print(question['question'])
        sys.stdout.flush()
        
        for c in question['choices']:
            print(question['choices'].index(c),c)
            sys.stdout.flush()
            
        playerAnswer = input()
        
        while playerAnswer not in ['0','1','2','3']:
            print('Y u so stupid? Please enter a valid choice: 0, 1, 2 or 3')
            sys.stdout.flush()
            playerAnswer = input()
        
        if int(playerAnswer) == question['choices'].index(question['answer']):
            print("CORRECT")
            sys.stdout.flush()
            score += 10
            
        else:
            print("WRONG... y u so stupid?")
            print('Answer: ', question['answer'])
            sys.stdout.flush()
        print()
        
    print("Your score is: ", score,"/ 100")
    sys.stdout.flush()
