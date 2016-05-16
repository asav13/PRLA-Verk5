import sys, json, argparse
import y_u_so_stupid

'''
    ARGUMENT PARSING
'''
parser = argparse.ArgumentParser(description='Y U so stupid!?')
parser.add_argument('-q', '--questions', help='number of questions to run', type=int, nargs=1, default=10)
parser.add_argument('-d', '--difficulty', help='difficulty,defined by number of choices', type=int, choices=range(2, 11), default=4)

args = parser.parse_args()

'''
    MAIN FUNCTION
'''
def playCLI():
    score = 0
    numberOfQuestions = args.questions
    if type(numberOfQuestions) == type([]):
        numberOfQuestions = numberOfQuestions[0]
    difficulty = args.difficulty
    
    printAndFlush("\n~Welcome to 'y u so stupid?'~\nNow, don't be stupid mkey?\n\nAre you ready?\n...\n")

    for i in range(numberOfQuestions):
        question = json.loads(y_u_so_stupid.getRandomQuestion(difficulty))

        printAndFlush(question['question'])
        
        for c in question['choices']:
            printAndFlush("{0}: {1}".format(question['choices'].index(c), c))

        try:
            playerAnswer = input()
            while (not playerAnswer.isnumeric()) or int(playerAnswer) not in range(difficulty):
                printAndFlush('y u so stupid..? Please enter a valid choice: {0}'.format(list(range(difficulty))))
                playerAnswer = input()
            printAndFlush("")
        except ValueError:
            printAndFlush("Dude, you pass in crap, y u so stupid? I say bye now!")
            break
        
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
